import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import pandas as pd

bot = Bot(token='5546689740:AAFuKh3kry1Ygfxcs399wgjc1xHMpzX9Ph4')  # создаю бота и указываю его токен
logging.basicConfig(level=logging.INFO)                            # включаю логирование, чтоб не упустить ошибки
dp = Dispatcher(bot)                                               # считыватель переписки с ботом (диспетчер)
data = pd.read_csv('movies_emotions.csv') # костыли
genre = data['Жанр'].values
emotion = data['Эмоция'].values
Callback = CallbackData('filter', 'option', 'action')              # создаю коллбэк для универсальной функции под кнопку
                                                                   # filter - название функции
                                                                   # option - выбор пользователя
                                                                   # action - действие кнопки (Выбор жанра или эмоции)

def DataFrame_to_String(data):                                     # Достаёт из data названия фильмов и помещает все в
    films = data['Название фильма'].unique()                       # в одну переменную, в разные строки через \n
    result = ''
    for film in films:
        result += film + '\n'
    return result


@dp.callback_query_handler(Callback.filter())                      # Обработка кнопки, создание фильтров
async def filter_DataFrame_on_emotion(call, callback_data):
    match callback_data['action']:
        case 'genre':
            global genre
            genre = callback_data['option']
        case 'emotion':
            global emotion
            emotion = callback_data['option']

    await call.message.answer('Вы выбрали - '+str(callback_data['option']))


@dp.message_handler(commands=['start', 'help'])                    # Главное меню с информацией
async def print_hi(message):
    await message.answer('Приветствую!\n'
                         'Я бот который поможет тебе выбрать фильм на вечер.'
                         '\nДля начала тебе нужно выбрать жанр фильм с которыми ты бы хотел видеть.\n'
                         'Для этого тебе ввести команду /genre и /emotion\n'
                         'А когда определишься со всеми жанрами и эмоциями введи команду /show')  # genre emotion


@dp.message_handler(commands='genre')                              # Выбор жанра
async def genre_filter(message):
    keyboard_of_genres = InlineKeyboardMarkup()                    # Объявление клавиатуры
    buttons = [InlineKeyboardButton(text='Драма', callback_data=Callback.new(option='Драма', action='genre')),
               InlineKeyboardButton(text='Боевик', callback_data=Callback.new(option='Боевик', action='genre')),
               InlineKeyboardButton(text='Фантастика', callback_data=Callback.new(option='Фантастика', action='genre')),
               InlineKeyboardButton(text='Приключения', callback_data=Callback.new(option='Приключения', action='genre')),
               InlineKeyboardButton(text='Комедия', callback_data=Callback.new(option='Комедия', action='genre')),
               InlineKeyboardButton(text='Криминал', callback_data=Callback.new(option='Криминал', action='genre')),
               InlineKeyboardButton(text='Семейный', callback_data=Callback.new(option='Семейный', action='genre')),
               InlineKeyboardButton(text='Фэнтази', callback_data=Callback.new(option='Фэнтази', action='genre')),
               InlineKeyboardButton(text='Ужасы', callback_data=Callback.new(option='Ужасы', action='genre'))]                                                # Создание кнопок в массиве (кидают на filter_DataFrame_on_emotion)
    keyboard_of_genres.add(*buttons)                               # Добавление всех кнопок в клавиатуру
    await message.answer('Выбери жанр:', reply_markup=keyboard_of_genres)


@dp.message_handler(commands='emotion')                            # Выбор эмоции
async def genre_filter(message):
    keyboard_of_emotions = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text='Странный', callback_data=Callback.new(option='Странный', action='emotion')),
               InlineKeyboardButton(text='Волнительный', callback_data=Callback.new(option='Волнительный', action='emotion')),
               InlineKeyboardButton(text='Вдохновляющий', callback_data=Callback.new(option='Вдохновляющий', action='emotion')),
               InlineKeyboardButton(text='Грустный', callback_data=Callback.new(option='Грустный', action='emotion')),
               InlineKeyboardButton(text='Добрый', callback_data=Callback.new(option='Добрый', action='emotion')),
               InlineKeyboardButton(text='Глупый', callback_data=Callback.new(option='Глупый', action='emotion')),
               InlineKeyboardButton(text='Страшный', callback_data=Callback.new(option='Страшный', action='emotion')),
               InlineKeyboardButton(text='Трогательный', callback_data=Callback.new(option='Трогательный', action='emotion')),
               InlineKeyboardButton(text='Страшный', callback_data=Callback.new(option='Страшный', action='emotion'))]
    keyboard_of_emotions.add(*buttons)
    await message.answer('Выбери жанр:', reply_markup=keyboard_of_emotions)


@dp.message_handler(commands='show')
async def show_DataFrame(message):                                 # Показывает результат
    filted_DataFrame = data[(data['Жанр'] == genre) & (data['Эмоция'] == emotion)] # Фильтрует датафрейм по фильтрам, что мы выставили
                                                                                   # если мы не выберали, он всё оставит без фильтрации
    await message.answer(DataFrame_to_String(filted_DataFrame))                    # Отправляет филтрованный датафрейм, преобразованный в строку


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)                  # Запускает проверку сообщений в диалоге (запускает бота)