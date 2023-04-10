from glob import glob
# импорты записываем в алфавитном порядке, что бы проще было искать
import os
from random import choice
from db import (db, get_or_create_user,
                subscribe_user, unsubscribe_user,
                save_cat_image_vote, user_voted,
                get_image_raiting)

from jobs import alarm
from utils import (play_random_numbers, main_keyboard, has_object_on_image, 
                   cat_rating_inline_keyboard)
# импортируем наши функции из utils


def greet_user(update, context):
    # функция приветсвтия пользователя
    print("Вызван start")
    # отображает текст в консоле
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    main_keyboard()
    # добавляем переменную  my_keyboard и ей присваиваем библиотку
    # ReplyKeyboardMarkup передаем функционал handlerhelper pussy
    update.message.reply_text(
        f'Здравствуй, пользователь {user["emoji"]}!',
        reply_markup=main_keyboard()  # создаем клавиатуру
    )


def talk_to_me(update, context):  # функция эхо бот
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    user_text = update.message.text
    # введенный текст обновляется в боте
    print(user_text)  # отображает текст в консоле
    update.message.reply_text(
        f'{user_text} {user["emoji"]}', reply_markup=main_keyboard()
        )
    # отображает клавиатуры для пользователя в телеграм боте


def guess_number(update, context):  # функция угадай число
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    if context.args:  # создается кортеж
        try:    # проверяем на ошибки
            user_number = int(context.args[0])
            # преобразовываем введеное число в целое
            message = play_random_numbers(user_number)
            # вызываем функцию сравнения числа
        except (TypeError, ValueError):  # ошибка если введено не целое число
            message = "Введите целое число"  # выводит сообщение об ошибке
    else:
        message = "Введите число"   # просит ввест число
    update.message.reply_text(message, reply_markup=main_keyboard())
    # отображает текст для пользователя в телеграм боте


def send_cat_picture(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    cat_photo_list = glob("images/cat*.jp*g")
    # берем список названий файлов только из папки /images
    # название файлов начинающихся на cat и имеет формат .jp*g
    cat_photo_filename = choice(cat_photo_list)  # случайное имя из списка
    chat_id = update.effective_chat.id
    # запрашиваем id пользователя в отдельную переменную
    if user_voted(db, cat_photo_filename, user["user_id"]):
        rating = get_image_raiting(db, cat_photo_filename)
        keyboard = None
        caption = f"рейтинг картинки {rating}"
    else:
        keyboard = cat_rating_inline_keyboard(cat_photo_filename)
        caption = None
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_photo_filename, "rb"),
        reply_markup=keyboard,
        caption=caption
    )
    # команда в библиотеке bot.send_photo которая отправляет картинку,
    # ей нужно 2 переменные, id пользователя и название картинки, rb -
    # открываем картинку для чтения в бинарном формате


def send_dog_picture(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    dog_photo_list = glob("images/dog*.jp*g")
    # берем список названий файлов только из папки /images
    # название файлов начинающихся на cat и имеет формат .jp*g
    dog_photo_filename = choice(dog_photo_list)  # случайное имя из списка
    chat_id = update.effective_chat.id
    # запрашиваем id пользователя в отдельную переменную
    context.bot.send_photo(chat_id=chat_id, photo=open(
        dog_photo_filename, "rb"), reply_markup=main_keyboard()
        )
    # команда в библиотеке bot.send_photo которая отправляет картинку,
    # ей нужно 2 переменные, id пользователя и название картинки, rb -
    # открываем картинку для чтения в бинарном формате


def user_coordinates(update, context):  # функция отправки координат
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    coords = update.message.location  # запрос координа
    update.message.reply_text(  # общение с пользователем
        f"Вашии координаты {coords}{user['emoji']}!",  # отправляем координаты
        reply_markup=main_keyboard  # отправляем клавиатуру
    )


def check_user_photo(update, context):  # функция по проверке фото
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    update.message.reply_text("Обрабатываем")
    os.makedirs("downloads", exist_ok=True)
    # импортирируем библиотек os для работы с файлами ей даем команду makedirs
    # - создать новую папку, назвать ее downloads, exist_ok=True - если такая
    # папка уже есть, то не будет создавать новую
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    # берем изображение -1 в наилучшем качестве, и берем его file_id
    file_name = os.path.join(
        "downloads", f"{update.message.photo[-1].file_id}.jpg"
        )
    # прописываем название файла, лучше делать через os.path.join, будет /\
    # использоваться на любой ОС
    photo_file.download(file_name)  # скачаем файл по адресу из file_name
    update.message.reply_text("Файл сохранен")  # сообщения для пользователя
    if has_object_on_image(file_name, "cat"):
        update.message.reply_text("Обнаружена киска, сохраняю в библиотеку")
        # сообщения для пользователя телеграм
        new_file_name = os.path.join("images", f"cat_{photo_file.file_id}.jpg")
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text("Тревога, киска не обнаружена!")


def subscribe(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    subscribe_user(db, user)
    update.message.reply_text("Вы успешно подписались")


def unsubscribe(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    unsubscribe_user(db, user)
    update.message.reply_text("Вы успешно отписались")


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f"Уведовмление через {alarm_seconds} секунд")
# run_once - запустить задачу 1 раз
# int - берем целое число, abs - берем по модулю
    except(ValueError, TypeError):
        update.message.reply_text("Введите целое число секунд после команды")


def cat_picture_rating(update, context):
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split("|")
    vote = int(vote)
    user = get_or_create_user(
        db, update.effective_user, update.effective_chat.id)
# что приходит от inline клавиатуры
    save_cat_image_vote(db, user, image_name, vote)
    rating = get_image_raiting(db, image_name)
    update.callback_query.edit_message_caption(caption=f"рейтинг картинки {rating}")
# edit_message_caption() - заменяет подписи
