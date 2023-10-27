# Инструкция по работе с Replit
[Replit](https://replit.com/) — популярная бесплатная онлайн-среда разработки, требующая совсем небольшой настройки перед созданием проектов. Этот редактор поддерживает больше 50 языков и используется на многих курсах по программированию.
## Как создать аккаунт в Replit
Для начала заходим на домашнюю страницу [Replit](https://replit.com/). В правом верхнем углу кликните:
- `Sign Up` - для регистрации (новых пользователей),
- `Log In` - для входа.

Для регистрации на сайте введите `username`, `email` и `пароль` или воспользуйтесь аккаунтом Google, Facebook или GitHub.
![Страница входа](https://techrocks.ru/wp-content/uploads/2021/11/Screen-Shot-2021-11-03-at-11.38.16-AM.png)

Войдя, вы попадете на домашнюю страницу своего аккаунта.
## Создать проект
Создадим проект `Create Repl` в верхнем левом углу.

![](https://ucarecdn.com/580a6511-de28-4880-9516-1354f0f0adef/)

Выберем шаблон `Flask` - это библиотека для создания веб-приложения на `Python`. Назовите проект, например `test-webhook`.

![image](https://github.com/yupest/nto/blob/master/NTO-2023/267651147-8544161e-4a1a-4729-9fd0-09f005bcfa09.png)

Допишим шаблон кода необхожимым и нажмем `Start`.

Пример кода:
```python
from flask import Flask, request, jsonify, make_response
import requests
import random

app = Flask(__name__)
# настройка поддержки кириллицы
app.config['JSON_AS_ASCII'] = False

# маршрут по умолчанию
@app.route('/')
def index():
    return 'Hello from Flask!'

def get_film(genre):
  # список фильмов по жанру
  films = requests.get(f'https://yupest2.pythonanywhere.com/api/v1.0/movies/?genre={genre}').json()['records']

  # случайный фильм в диапазоне от нулевого до последнего из списка
  film = films[random.randint(0, len(films)-1)]

  # строка ответа бота с рекомендацией фильма
  return '{} в жанре {}, сделан в стране: {} с рейтингом: {}'.format(film['Название'], film['Жанр'], film['Страна'], film['Средняя оценка'])

def get_result():
  # извлечение параметра
  req = request.get_json(force=True)
  result = req.get("queryResult")
  parameters = result.get("parameters")
  # название параметра в соответствии с названием параметра сущности в интенте Genres
  # здесь можно задать переменные для каждого параметра, если их несколько
  genre = parameters.get("genre")

  # если параметр задан, вернем случайный фильм
  if genre:
    return {'fulfillmentText': get_film(genre)}

# маршрут webhook
@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
  return make_response(jsonify(get_result()))

app.run(host='0.0.0.0', port=5000)
```

## Настройка Webhook в Dialogflow

Скопируем ссылку в проекте Replit

![](https://ucarecdn.com/b672e90e-2e97-48cd-aaaa-7f72913d8acd/)

Скопированная ссылка необходима при настройке `Webhook` в разделе `Fulfillment` в `Dialogflow`. Допишем к ней `/webhook` и не забудьте сохраниться (`Save` внизу страницы)
![](https://ucarecdn.com/0f9e88f9-d2b3-4eba-8d9d-5b8319a65109/)

Приступим к тестированию:

<img src='https://ucarecdn.com/7592384f-ee92-4d1a-b46a-2a0055d0de56/' width = 450><img src='https://ucarecdn.com/457d2777-e6e0-4c38-9735-a1349ccdc217/' width = 500>
