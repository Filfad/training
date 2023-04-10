from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
# удалим клавиатуру, в этом окне она не нужна, ParseMode- форматировать текст
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_anketa
from utils import main_keyboard  # завершаем нашу анкету


def anketa_start(update, context):
    update.message.reply_text(  # на экране появляется вопрос пользователю
        "Как вас зовут? Напишите имя и фамилию",
        reply_markup=ReplyKeyboardRemove()  # удаляем клавиатуру
    )
    return "name"


def anketa_name(update, context):
    user_name = update.message.text
    # update.message.text в переменную ввел пользователь
    # провереяем, если пользователь ввел что-то меньше 2-ух слов
    if len(user_name.split()) < 2:  # сплит разделение по пробелу,если < 2
        update.message.reply_text("Пожалуйста введите имя и фамилию")
        # выдаем сообщение об ошибке
        return "name"
    # снова запрашивает имя (по кругу, пока не введет имя и фамилию)
    else:
        context.user_data["anketa"] = {"name": user_name}
        # хранилище куда можем сохранить данные у конкретного пользователя
        # словарь анкета, name - ключ, user_name - значение
        reply_keyboard = [["1", "2", "3", "4", "5"]]
        # надписи на клавиатуре для оценки
        update.message.reply_text(  # вопрос к пользователю
            "Пожалуйста оцените наше бота от 1 до 5",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
                # передаем клавиатуру one_time_keyboard=True -
                # клавиатура показана 1 раз, как на нее нажмет она уйдет
            )

        )
        return "rating"  # переход к следующему шагу


def anketa_rating(update, context):
    context.user_data["anketa"]["rating"] = int(update.message.text)
    update.message.reply_text(
        "Напишите комментарий, или нажмите /skip что бы пропустить"
        )
    return "comment"


def anketa_comment(update, context):
    context.user_data["anketa"]["comment"] = update.message.text
    # в комменте сохранеяем текст который ввел пользователь
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    save_anketa(db, user["user_id"], context.user_data["anketa"])
    user_text = format_anketa(context.user_data["anketa"])

    update.message.reply_text(
        user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
        )
    # reply_markup=main_keyboard() - выводим основную клавиатуру,
    # parse_mode=ParseMode.HTML текст выдаем в формате HTML
    return ConversationHandler.END
    # завершаем нашу анкету(диалог)


def anketa_skip(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id
        )
    save_anketa(db, user["user_id"], context.user_data["anketa"])
    user_text = format_anketa(context.user_data["anketa"])
    update.message.reply_text(
        user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
        )
    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f"""<b>Имя Фамилия:</b> {anketa['name']}
<b>Оценка:</b> {anketa['rating']}"""
    if ('comment') in anketa:
        user_text += f"\n<b>Комментарий:</b> {anketa['comment']}"
    return user_text


def anketa_dontknow(update, context):
    update.message.reply_text("Я Вас не понимаю")
