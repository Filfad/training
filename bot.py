import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
from handlers import (greet_user, guess_number, send_cat_picture, send_dog_picture, user_coordinates, talk_to_me)
logging.basicConfig(filename='bot.log', level=logging.INFO) #запись в реестр 
import settings

def main():
    mybot =  Updater(settings.API_KEY, use_context=True) 
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start",greet_user))
    dp.add_handler(CommandHandler("guess",guess_number))
    dp.add_handler(CommandHandler("pussy",send_cat_picture)) #добавляем CommandHandler команду cat, когда пишем в телеграме команду cat telegram знает что нам нужно отослать функцию send_cat_picture по отправке картинок котиков
    dp.add_handler(CommandHandler("dog",send_dog_picture)) #добавляем CommandHandler команду cat, когда пишем в телеграме команду cat telegram знает что нам нужно отослать функцию send_cat_picture по отправке картинок котиков
    dp.add_handler(MessageHandler(Filters.regex('^(Показать киску)$'),send_cat_picture)) # реагируем только на эту фразу '^(Прислать котика)$'  ^-начало фразы $ - конец фразы
    dp.add_handler(MessageHandler(Filters.regex('^(Показать песеля)$'),send_dog_picture)) # реагируем только на эту фразу '^(Прислать котика)$'  ^-начало фразы $ - конец фразы
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
if __name__ == "__main__":
    main()