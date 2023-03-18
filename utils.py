# Import the Clarifai gRPC-based objects needed
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2 # This is how you authenticate
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
def has_object_on_image(file_name, object_name): #ищем на картинке object name
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)
    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
    
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    #print(response)
    return check_response_for_object(response, object_name)

def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS: #если обработка картинки удачна
        for concept in response.outputs[0].data.concepts: # проходим по всем concepts
            if concept.name ==object_name and concept.value >= 0.85: #если нашли концепт где есть cat и уверенность 85%
                return True
    else:
        print(f"Ошибка распознования картинки{response.outputs[0].status.details}")    
    return False
if __name__ == "__main__":
    print(has_object_on_image('images/cat1.jpg', "dog"))
    print(has_object_on_image('images/dog1.jpeg', "dog"))
    print(has_object_on_image('images/dogprichini.jpg', "dog"))

"""
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2# This is how you authenticate.
metadata = (('authorization', 'Key #{{YOUR_CLARIFAI_API_KEY}}'),)
with open("{YOUR_IMAGE_FILE_LOCATION}", "rb") as f:
    file_bytes = f.read()
    
request = service_pb2.PostModelOutputsRequest(
    model_id='aaa03c23b3724a16a56b629203edc62c',
    inputs=[
        resources_pb2.Input(
            data=resources_pb2.Data(
                image=resources_pb2.Image(
                    base64=file_bytes
                )
            )
        )      
    ])
response = stub.PostModelOutputs(request, metadata=metadata)
if response.status.code != status_code_pb2.SUCCESS:
    raise Exception("Request failed, status code: " + str(response.status.code))for concept in response.outputs[0].data.concepts:
print('%12s: %.2f' % (concept.name, concept.value))
"""