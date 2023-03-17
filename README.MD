# Проект catbot
 CatBot - это бот для Telegram, который показывает пользователем киску
 ## Установка
 
 1. Клонируем репозиторий с github 
 2. Создаем виртуальное окружение
 3. Устанавливаем зависимости `pip install -r requirements.txt`
4. Создание файла `settings.py`
5. Впишем в `settings.py` переменные:
```
API_KEY = "API-ключ бота"
USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:'] #списко случайных смайлов для вызова 
```
6. Запустить бота командоай `python bot.py`
    