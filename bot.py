from emoji import emojize
from glob import glob #импорты записываем в алфавитном порядке, что бы проще было искать
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO) #запись в реестр 

def greet_user(update, context): #функция приветсвтия пользователя
    print("Вызван \start") #отображает текст в консоле
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f'Здравствуй, пользователь {context.user_data["emoji"]}!') #отображает текст для пользователя в телеграм боте

def talk_to_me(update, context): #функция эхо бот
    context.user_data["emoji"] = get_smile(context.user_data) #запомнить какие-то данные о пользователе, Это словарь: если мы добавим в него ключ с данными, эти данные будут доступны для этого пользователя.
    user_text = update.message.text #введенный текст обновляется в боте
    print(user_text) #отображает текст в консоле
    update.message.reply_text(f'{user_text} {context.user_data["emoji"]}') #отображает текст для пользователя в телеграм боте

def get_smile(user_data):
    if "emoji" not in user_data:
        smile = choice(settings.USER_EMOJI) #переменная smile берет случайное значение из списка USER_EMOJI находящегося в файле settings
        return emojize(smile, language ='alias')#emojize переводит текст смайлика в смайлик,use_aliases = True использовать формат смайлика ":shit:"
    return user_data["emoji"]

def play_random_numbers(user_number): #функция создает рандомное число и сравнивает его с пользовательским
    bot_number = randint(user_number - 10,user_number + 10)#генерируется случайное число -+10 от числа пользователя
    if user_number > bot_number: #сравниваем числа и кто выиграл 
        message = f"Твое число {user_number}, мое {bot_number},  вы выиграли"
    elif user_number == bot_number:
        message = f"Твое число {user_number}, мое {bot_number},  ничья"
    else:
        message = f"Твое число {user_number}, мое {bot_number},  вы проиграли"
    return message #возвращает сообщение в функцию

def guess_number(update, context):#функция угадай число
    print(context.args) #отображает текст в консоле
    if  context.args: #создается кортеж
        try:    #проверяем на ошибки
            user_number = int(context.args[0]) #преобразовываем введеное число в целое 
            message = play_random_numbers(user_number) #вызываем функцию сравнения числа 
        except(TypeError, ValueError): #ошибка если введено не целое число
            message = "Введите целое число" #выводит сообщение об ошибке
    else:   
        message = "Введите число"   #просит ввест число
    update.message.reply_text(message) #отображает текст для пользователя в телеграм боте

def send_cat_picture(update, context):
    cat_photo_list = glob("images/cat*.jp*g") #берем список названий файлов только из папки /images название файлов начинающихся на cat и имеет формат .jp*g
    cat_photo_filename = choice(cat_photo_list) #случайное одно имя из списка имен
    chat_id = update.effective_chat.id #запрашиваем id пользователя в отдельную переменную
    context.bot.send_photo(chat_id = chat_id, photo = open (cat_photo_filename,"rb")) #команда в библиотеке bot.send_photo которая отправляет картинку, ей нужно 2 переменные, id пользователя и название картинки, rb - открываем картинку для чтения в бинарном формате 

def main():
    mybot =  Updater(settings.API_KEY, use_context=True) 
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start",greet_user))
    dp.add_handler(CommandHandler("guess",guess_number))
    dp.add_handler(CommandHandler("pussy",send_cat_picture)) #добавляем CommandHandler команду cat, когда пишем в телеграме команду cat telegram знает что нам нужно отослать функцию send_cat_picture по отправке картинок котиков
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
if __name__ == "__main__":
    main()