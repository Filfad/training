from datetime import time
import logging
import pytz

from telegram.bot import Bot
from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters, ConversationHandler,
    CallbackQueryHandler)
from telegram.ext import messagequeue as mq
from telegram.ext.jobqueue import Days
from telegram.utils.request import Request
from anketa import (anketa_start, anketa_name, anketa_rating,
                    anketa_comment, anketa_skip, anketa_dontknow)
# импортируем из файла anketa функцию ankta_start()
from handlers import (
    greet_user, guess_number, send_cat_picture, send_dog_picture,
    user_coordinates, talk_to_me, check_user_photo, subscribe, unsubscribe,
    set_alarm, cat_picture_rating)
from jobs import send_updates
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)
# запись в реестр


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):  # когда бот останавливается
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage  # декоратор
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)


def main():
    request = Request(con_pool_size=8)  # 8 соединенеий
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot, use_context=True)
    jq = mybot.job_queue
    target_time = time(12, 0, tzinfo=pytz.timezone("Europe/Moscow"))
    target_days = (Days.MON, Days.WED, Days.FRI)
    jq.run_daily(send_updates, target_time, target_days)
    # каждые 10 сек. interval=10  выполняй функцию send_updates
    # first=0 - когда начинается
    dp = mybot.dispatcher
    anketa = ConversationHandler(  # добавляем ConversationHandler для анкеты
        entry_points=[
            # entry_points – это точка входа, запускающая диалог.
            # Состоит из списка Handler-ов, и если один из них сработает –
            # бот начнет отработку данного диалога.
            MessageHandler(Filters.regex("^(Заполнить анкету)$"), anketa_start)
        ],
        # вход в анкету
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            # бот принимает ответ в анкете
            "rating": [MessageHandler(
                Filters.regex('^(1|2|3|4|5)$'), anketa_rating
                )],
            # бот принимает ответ на рейтенг 1-5
            "comment": [CommandHandler("skip", anketa_skip),
                        MessageHandler(Filters.text, anketa_comment)]
        },
        fallbacks=[MessageHandler(Filters.text | Filters.photo | Filters.video
                                  | Filters.location, anketa_dontknow)]
        # если предыдующие handler не отработают, выдаст ошибку
        # fallbacks – срабатывает, когда вводит что-то неподходящее.
        # Также можно при помощи fallbacks делать выход из диалога
        )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("pussy", send_cat_picture))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("alarm", set_alarm))
    dp.add_handler(CallbackQueryHandler(cat_picture_rating, pattern="^(raiting|)"))
    # добавляем CommandHandler команду cat, когда пишем в телеграме
    # команду cat telegram знает что нам нужно отослать функцию
    # send_cat_picture по отправке картинок котиков
    dp.add_handler(CommandHandler("dog", send_dog_picture))
    # добавляем CommandHandler команду cat, когда пишем в телеграме команду
    # cat telegram знает что нам нужно отослать функцию send_cat_picture по
    # отправке картинок котиков
    dp.add_handler(MessageHandler(Filters.regex('^(Показать киску)$'),
                                  send_cat_picture))
    # реагируем на фразу '^(Прислать котика)$'  ^-начало фразы $ - конец фразы
    dp.add_handler(MessageHandler(Filters.regex('^(Показать песеля)$'),
                                  send_dog_picture))
    # реагируем на фразу '^(Прислать котика)$'  ^-начало фразы $ - конец фразы

    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    # MessageHandler проверяющий фото от пользователя
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
