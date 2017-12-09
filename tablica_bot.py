import telebot

bot = telebot.TeleBot("456403564:AAFLQjaNSumXGcd9hl_nEbCZyvIFdNmFCHk")

step = 0

global office_words
office_words = ["ОФИС", "ОФИСА" , "ОФИСНОЕ", "ОФИСНЫЕ"]
coworking_words = ["КОВОРКИНГ"]
yes_words = ["ДА","ХОЧУ","БУДУ","НАВЕРНОЕ","ВОЗМОЖНО"]

global answers

answers = {
    "office_1": "Я покажу что у нас есть, сколько человек у вас в команде ?",
    "office_2": "У нас офисы от 4 человек, показать тебе офисы на четверых или рассказать о коворкинге ?",
    "office_3": "Вот что у нас есть на четверых",
    "coworking_1": "Мы предлагаем плавающее рабочее место от 500 рублей в день, хочешь забронировать ?"
    "coworking_2": "Оставь телефон и мы тебе перезвоним"
}

urls = {
    "office_1": "",
    "office_2": "",
    "office_3": "http://tablica.work/#office#!/tproduct/34756154-1507644732627", # офис на четверых
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
#splitting text into keywords

    keywords = [x for x in text.split()]

    print(keywords)
    print(office_words)
    print(step)



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
            if number_of_empl = 4:
                step = "office_3"
                answer = answers[step]
                bot.send_message(message.chat.id, answer)
                bot.send_message(message.chat.id, "http://tablica.work/#office#!/tproduct/34756154-1507644732627")

    # если на шаге office2 клиент все же хочет посмотреть офисы - показываем офисы на четверых
    if step == "office_2" and bool(set(keywords) & set(office_words)):
        step = "office_3"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)
        answer = urls[step]
        bot.send_message(message.chat.id, answer)

    if step == "office_3" and bool(set(keywords) & set(coworking_words)):
        step = "coworking_1"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)

    if step == "coworking_1" and bool(set(keywords) & set(yes_words)):
        step = "coworking_2"
        answer = answers[step]
        bot.send_message(message.chat.id, answer)




    #bot.send_message(message.chat.id, url)
    #bot.send_photo(chat_id = message.chat.id, photo = url)

 #@bot.message_handler(content_types=['location'])



bot.polling()