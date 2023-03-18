from glob import glob #импорты записываем в алфавитном порядке, что бы проще было искать
import os
from random import choice
from utils import (get_smile, play_random_numbers, main_keyboard, has_object_on_image) #импортируем наши функции из utils 

def greet_user(update, context): #функция приветсвтия пользователя
    print("Вызван \start") #отображает текст в консоле
    context.user_data["emoji"] = get_smile(context.user_data)
    main_keyboard() #добавляем переменную  my_keyboard и ей присваиваем библиотку ReplyKeyboardMarkup передаем функционал handlerhelper pussy
    update.message.reply_text(
        f'Здравствуй, пользователь {context.user_data["emoji"]}!',
        reply_markup = main_keyboard() # создаем клавиатуру
    ) 

def talk_to_me(update, context): #функция эхо бот
    context.user_data["emoji"] = get_smile(context.user_data) #запомнить какие-то данные о пользователе, Это словарь: если мы добавим в него ключ с данными, эти данные будут доступны для этого пользователя.
    user_text = update.message.text #введенный текст обновляется в боте
    print(user_text) #отображает текст в консоле
    update.message.reply_text(f'{user_text} {context.user_data["emoji"]}',
        reply_markup = main_keyboard()) #отображает клавиатуры для пользователя в телеграм боте

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
    update.message.reply_text(message, reply_markup = main_keyboard()) #отображает текст для пользователя в телеграм боте

def send_cat_picture(update, context):
    cat_photo_list = glob("images/cat*.jp*g") #берем список названий файлов только из папки /images название файлов начинающихся на cat и имеет формат .jp*g
    cat_photo_filename = choice(cat_photo_list) #случайное одно имя из списка имен
    chat_id = update.effective_chat.id #запрашиваем id пользователя в отдельную переменную
    context.bot.send_photo(chat_id = chat_id, photo = open (cat_photo_filename,"rb"),reply_markup = main_keyboard()) #команда в библиотеке bot.send_photo которая отправляет картинку, ей нужно 2 переменные, id пользователя и название картинки, rb - открываем картинку для чтения в бинарном формате 

def send_dog_picture(update, context):
    dog_photo_list = glob("images/dog*.jp*g") #берем список названий файлов только из папки /images название файлов начинающихся на cat и имеет формат .jp*g
    dog_photo_filename = choice(dog_photo_list) #случайное одно имя из списка имен
    chat_id = update.effective_chat.id #запрашиваем id пользователя в отдельную переменную
    context.bot.send_photo(chat_id = chat_id, photo = open (dog_photo_filename,"rb"),reply_markup = main_keyboard()) #команда в библиотеке bot.send_photo которая отправляет картинку, ей нужно 2 переменные, id пользователя и название картинки, rb - открываем картинку для чтения в бинарном формате 

def user_coordinates(update,context): #функция отправки координат 
    context.user_data["emoji"] = get_smile(context.user_data)
    coords = update.message.location #запрос координа 
    update.message.reply_text( #общение с пользователем 
        f"Вашии координаты {coords}{context.user_data['emoji']}!",#отправляем координаты
        reply_markup = main_keyboard #отправляем клавиатуру
    )

def check_user_photo(update, context): #функция по проверке фото 
    update.message.reply_text("Обрабатываем")
    os.makedirs("downloads", exist_ok=True ) #импортирируем библиотек os для работы с файлами ей даем команду makedirs - создать новую папку, назвать ее downloads, exist_ok=True - если такая папка уже есть, то не будет создавать новую
    photo_file = context.bot.getFile(update.message.photo[-1].file_id) #берем изображение -1 в наилучшем качестве, и берем его file_id
    file_name = os.path.join("downloads", f"{update.message.photo[-1].file_id}.jpg") #прописываем название файла, лучше делать через os.path.join, будет /\ использоваться на любой ОС
    photo_file.download(file_name)#скачаем файл по адресу из file_name
    update.message.reply_text("Файл сохранен") #сообщения для пользователя телеграм
    if has_object_on_image(file_name,"cat"):
        update.message.reply_text("Обнаружена киска, сохраняю в библиотеку")#сообщения для пользователя телеграм
        new_file_name = os.path.join("images", f"cat_{photo_file.file_id}.jpg")
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text("Тревога, киска не обнаружена!")