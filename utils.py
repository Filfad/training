# Import the Clarifai gRPC-based objects needed
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
# This is how you authenticate

from random import randint
# random
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# клавиатура для бота, специальная кнопка для геолокации
import settings


def play_random_numbers(user_number):
    # функция создает рандомное число и сравнивает его с пользовательским
    bot_number = randint(user_number - 10, user_number + 10)
    # генерируется случайное число -+10 от числа пользователя
    if user_number > bot_number:  # сравниваем числа и кто выиграл
        message = f"Твое число {user_number}, мое {bot_number},  вы выиграли"
    elif user_number == bot_number:
        message = f"Твое число {user_number}, мое {bot_number},  ничья"
    else:
        message = f"Твое число {user_number}, мое {bot_number},  вы проиграли"
    return message  # возвращает сообщение в функцию


def main_keyboard():  # добавляем переменную  my_keyboard и ей присваиваем
    # библиотку ReplyKeyboardMarkup передаем функционал handlerhelper pussy
    return ReplyKeyboardMarkup([
        ["Заполнить анкету",
         KeyboardButton("Мое расположение", request_location=True)],
        # добавили кнопку заполнить передает расположение пользователя с
        # помощью, KeyboardButton("мое расположение", request_location = True)
        ["Показать песеля", "Показать киску"]
                                ])


def has_object_on_image(file_name, object_name):  # ищем на фото objectname
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)
    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
    request = service_pb2.PostModelOutputsRequest(
        model_id=settings.CLARIFAI_MODEL_ID,
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    # print(response)
    return check_response_for_object(response, object_name)


def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        # если обработка картинки удачна
        for concept in response.outputs[0].data.concepts:
            # проходим по всем concepts
            if concept.name == object_name and concept.value >= 0.85:
                # если нашли концепт где есть cat и уверенность 85%
                return True
    else:
        print(f"Ошибка распознования {response.outputs[0].status.details}")
    return False


def cat_rating_inline_keyboard(image_name):
    callback_text = f"rating|{image_name}|"
    keyboard = [
        [
            InlineKeyboardButton("Нравится",
                                 callback_data=callback_text + "1"),
            InlineKeyboardButton("Не нравится",
                                 callback_data=callback_text + "-1"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


if __name__ == "__main__":
    print(has_object_on_image('images/cat1.jpg', "dog"))
    print(has_object_on_image('images/dog1.jpeg', "dog"))
    print(has_object_on_image('images/dogprichini.jpg', "dog"))
