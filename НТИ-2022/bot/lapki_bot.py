from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import logging

TOKEN = '...'
bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
data = pd.read_csv('lapkins.csv')
data["Продолжительность жизни среднее"] = data[['Продолжительность жизни макс','Продолжительность жизни мин']].mean(axis=1)
data["Вес среднее"] = data[['Вес макс', 'Вес мин']].mean(axis=1)
data["Рост среднее"] = data[['Рост макс','Рост мин']].mean(axis = 1)


def data_to_string(data):
    titles = data['Название породы'].unique()  # в одну переменную, в разные строки через \n
    result = ''
    for title in titles:
        result += title + '\n'
    return result


class UserState(StatesGroup):
    active = State()
    friendly = State()


@dp.message_handler(commands=['start','help','menu'])
async def menu(message):
    await message.reply('Привет, хочешь выбрать собачку?)\n Если да, то введи /option')


@dp.message_handler(commands='option')
async def menu(message):
    await message.answer('Напиши насколько активную собаку ты хочешь по 10-бальной шкале?')
    await UserState.active.set()


@dp.message_handler(state=UserState.active)
async def get_username(message, state):
    await state.update_data(active=message.text)
    await message.answer("Отлично! А на сколько дружелюбную?")
    await UserState.next() # либо же UserState.address.set()


@dp.message_handler(state=UserState.friendly)
async def get_address(message, state):
    await state.update_data(friendly=message.text)
    data_2 = await state.get_data()
    try:
        global result_data
        result_data = data[(data['Активность']==int(data_2['active']))&(data['Дружелюбность']==int(data_2['friendly']))]
        keyboard = InlineKeyboardMarkup()
        buttons = [
            InlineKeyboardButton(text='Средний вес', callback_data='Вес среднее'),
            InlineKeyboardButton(text='Средний рост', callback_data='Рост среднее'),
        ]
        buttons2 = [InlineKeyboardButton(text='Продолжительность жизни среднее', callback_data='Продолжительность жизни среднее')]
        keyboard.add(*buttons).add(*buttons2)
        await message.answer('Выбери по чему сортировать:', reply_markup=keyboard)
    except:
        await message.answer('Извини, но таких собак нет(\n'
                             'Используй ещё раз /option')

    await state.finish()


@dp.callback_query_handler(text=['Вес среднее', 'Рост среднее', 'Продолжительность жизни среднее'])
async def result(callback):
    try:
        print(result_data.sort_values(callback.data, ascending=False))
        await callback.message.answer(data_to_string(result_data.sort_values(callback.data, ascending=False)))
    except:
        await callback.message.answer('Таких собак нет, увы(')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)