import telebot

bot = telebot.TeleBot("456403564:AAFLQjaNSumXGcd9hl_nEbCZyvIFdNmFCHk")

step = 0

office_words = ["ОФИС", "ОФИСА" , "ОФИСНОЕ", "ОФИСНЫЕ"]
coworking_words = ["КОВОРКИНГ"]
event_words = ["МЕРОПРИЯТИЕ", "ПРЕЗЕНТАЦИЯ","КОНФЕРЕНЦИЯ","ПРЕЗЕНТАЦИЮ","КОНФЕРЕНЦИЮ","ТРЕНИНГ","КУРСЫ","ПЛОЩАДКА","ПОМЕЩЕНИЕ","ПЛОЩАДКУ","ПЛОЩАДКИ","КОРПОРАТИВНАЯ","ВЕЧЕРИНКА"]
date_words = ["ЯНВАРЯ","ФЕВРАЛЯ","МАРТА","АПРЕЛЯ","МАЯ","ИЮНЯ","ИЮЛЯ","АВГУСТА","СЕНТЯБРЯ","ОКТЯБРЯ","НОЯБРЯ","ДЕКАБРЯ"]


yes_words = ["ДА","ХОЧУ","БУДУ","НАВЕРНОЕ","ВОЗМОЖНО"]

support_chat_id = "-239908850" # id чата куда шлем заявки

answers = {
    "office_1": "Я покажу что у нас есть, сколько человек у вас в команде ?",
    "office_2": "У нас офисы от 4 человек, показать тебе офисы на четверых или рассказать о коворкинге ?",
    "office_3": "Вот что у нас есть на четверых",
    "office_4": "Вот что у нас есть на пятерых",
    "coworking_1": "Мы предлагаем плавающее рабочее место от 500 рублей в день, хочешь забронировать ?",
    "coworking_2": "Оставь телефон и мы тебе перезвоним",
    "coworking_3": "Спасибо, жди звонка!",
    "event_1": "Мы можем вместить до 150 человек - сколько вас будет ?",
    "event_2": "круто, когда планируете мероприятие ?",
    "event_3": "сколько часов потребуется ?",
}

urls = {
    "office_1": "",
    "office_2": "",
    "office_3": "http://tablica.work/#office#!/tproduct/34756154-1507644732627", # офис на четверых
    "office_4": "http://tablica.work/#!/tproduct/34756154-1498486301712", # офис на пятерых
    "coworking_1": ""
}

#handling start or help command
@bot.message_handler(commands=['start','help'])
def start_command(message: telebot.types.Message):
    #message_dict = message.__dict__
    startText = "Привет! Я - Бот Таблицы и я много чего могу ! Что тебя интересует ?"

    bot.send_message(message.chat.id, startText)

#handling /commands
@bot.message_handler(commands=['commands'])
def commands(message: telebot.types.Message):
    commands = ["/start", "/help", "/office", "/coworking", "/event"]
    answer = "\n".join(commands)
    bot.send_message(message.chat.id,answer)

#handling free text message
@bot.message_handler()
def free_text(message: telebot.types.Message):

    global step

#extracting tet from message object + make it uppercase
    text = message.text
    print(text)
    text = text.upper()
    print(text)
    print(message.chat.id)
#splitting text into keywords

    keywords = [x for x in text.split()]

    print(keywords)
    print(office_words)
    print(step)


# обрабатываем запрос офиса

    if step == 0 and bool(set(keywords) & set(office_words)):
        step = "office_1"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)


# спросим сколько человек в команде и предложим офис на соответствующее кол-во сотрудников:
    # меньше 4 - предложим офис на четверых или иныу о коворкинге
    if step == "office_1":
        if keywords[0].isdigit():
            number_of_empl = int(keywords[0])
            if number_of_empl < 4:
                step = "office_2"
                answer = answers[step]
                bot.send_message(message.chat.id, answer)

    # 4 - предложим офис на четверых
    if step == "office_1":
        if keywords[0].isdigit():
            number_of_empl = int(keywords[0])
            if number_of_empl == 4:
                step = "office_3"
                answer = answers[step]
                bot.send_message(message.chat.id, answer)
                answer = urls[step]
                bot.send_message(message.chat.id, answer)

    # 5 - предложим офис на пятерых
    if step == "office_1":
        if keywords[0].isdigit():
            number_of_empl = int(keywords[0])
            if number_of_empl == 4:
                step = "office_4"
                answer = answers[step]
                bot.send_message(message.chat.id, answer)
                answer = urls[step]
                bot.send_message(message.chat.id, answer)

    # ну и так далее тут дописать офисы



    # если на шаге office2 клиент все же хочет посмотреть офисы - показываем офисы на четверых
    if step == "office_2" and bool(set(keywords) & set(office_words)):
        step = "office_3"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)
        answer = urls[step]
        bot.send_message(message.chat.id, answer)

    # а если таки решил что интереснее коворкинг - разговариваем с ним о коворкинге и стреляем телефон. Контакт отправляем в специальный
    # чатик

    if step == "office_2" and bool(set(keywords) & set(coworking_words)):
        step = "coworking_1"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)

    if step == "coworking_1" and bool(set(keywords) & set(yes_words)):
        step = "coworking_2"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)

    if step == "coworking_2" and keywords[0][1:].isdigit():
        step = "coworking_3"
        opportunity_contact_dict = {"text" : message.text , "user_id": message.chat.id, "step" : step}
        opportunity_contact_text = '\n'.join(['%s:: %s' % (key, value) for (key, value) in opportunity_contact_dict.items()])
        bot.send_message(support_chat_id, opportunity_contact_text)
        answer = answers[step]
        bot.send_message(message.chat.id, answer)

    # обрабатываем запрос мероприятия

    if step == 0 and bool(set(keywords) & set(event_words)):
        step = "event_1"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)

    if step == "event_1" and keywords[0].isdigit():
        if int(keywords[0]) < 151:
            event_participants = message.text
            step = "event_2"
            answer = answers[step]
            bot.send_message(message.chat.id, answer)

    if step == "event_2" and bool(set(keywords) & set(date_words)):
        event_date = message.text
        step = "event_3"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)

    if step == "event_3" and bool(set(keywords) & set(date_words)):
        event_date = message.text
        step = "event_4"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)


    #bot.send_message(message.chat.id, url)
    #bot.send_photo(chat_id = message.chat.id, photo = url)

 #@bot.message_handler(content_types=['location'])



bot.polling()