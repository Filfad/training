from emoji import emojize
from random import choice, randint #random 
from telegram import ReplyKeyboardMarkup, KeyboardButton #клавиатура для бота, специальная кнопка для геолокации 
import settings

def get_smile(user_data):
    if "emoji" not in user_data: #если смайлика нет, то мы его присваиваем
        smile = choice(settings.USER_EMOJI) #переменная smile берет случайное значение из списка USER_EMOJI находящегося в файле settings
        return emojize(smile, language ='alias')#emojize переводит текст смайлика в смайлик,use_aliases = True использовать формат смайлика ":shit:"
    return user_data["emoji"] #возвращаем смайл

def play_random_numbers(user_number): #функция создает рандомное число и сравнивает его с пользовательским
    bot_number = randint(user_number - 10,user_number + 10)#генерируется случайное число -+10 от числа пользователя
    if user_number > bot_number: #сравниваем числа и кто выиграл 
        message = f"Твое число {user_number}, мое {bot_number},  вы выиграли"
    elif user_number == bot_number:
        message = f"Твое число {user_number}, мое {bot_number},  ничья"
    else:
        message = f"Твое число {user_number}, мое {bot_number},  вы проиграли"
    return message #возвращает сообщение в функцию

def main_keyboard(): #добавляем переменную  my_keyboard и ей присваиваем библиотку ReplyKeyboardMarkup передаем функционал handlerhelper pussy
    return ReplyKeyboardMarkup([
        ["Показать киску", KeyboardButton("Мое расположение", request_location = True)], # передает расположение пользователя с помощью, KeyboardButton("мое расположение", request_location = True)
        ["Показать песеля"]
                                ])   