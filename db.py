from random import choice
from emoji import emojize
from pymongo import MongoClient
import settings
client = MongoClient(settings.MONGO_LINK)

#collection - таблица
db = client[settings.MONGO_DB]

#функция, которая сохраняет в базу пользователя, если там такого еще нет и возвращает нам его данные

def get_or_create_user(db, effective_user, chat_id): #effective user - пользователь который пишет в чате
    user = db.users.find_one({"user_id":effective_user.id})#проверяем есть ли user в базе, effective user - присылает телеграм
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "emoji": emojize(choice(settings.USER_EMOJI), language ='alias')

        }
        db.users.insert_one(user)
    return user
