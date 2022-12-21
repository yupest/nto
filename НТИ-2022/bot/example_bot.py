# загрузка модулей
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import random

# Инициализируем бота
bot = Bot(token='5775826366:AAHpzS1C7JP8lZ8dnMlob36tht-DwK8MLB0')

storage = MemoryStorage()
# Инициализируем диспетчер сообщений
dp = Dispatcher(bot, storage = storage)

# списки и словари тематических шуток, загадок и фактов
riddles = {'Кто является автором книги "Гарри Поттер и философский камень"?': 'Джоан Роулинг',
            # и другие загадки в этом виде...
          }
jokes   = ["Что делает книга, когда ее потеряли? Она ищет себя!",
            # и другие шутки в этом виде...
          ] 

facts = {'другое':[
                    'Одна из самых ранних известных книг - это "Египетские мумии", написанные на древнеегипетском языке из цилиндрических сейфов, которые были найдены в Египте. Они были написаны около 2500 лет до н.э.',
                   'Книга, которая чаще всего считается самой древней в мире, - это "И-Шугур", сохранившаяся в виде таблиц с символами на клинописном шрифте. Она была найдена в Шумере и написана около 4000 лет до н.э.'],
         'джоан роулинг':r'Одной из самых популярных книг в мире является "Гарри Поттер и философский камень", на работу над которой автор Дж.К. Роулинг начала в 1990 году и выпустила ее в 1997 году. Это первая книга из серии о Гарри Поттере, которая стала одной из самых продаваемых в мире и была переведена на более чем 70 языков.'}

# установка класса состояний
class UserState(StatesGroup):
    variable = State()
#   создаем столько переменных, сколько потребуется

# возможные ответы пользователя
positive_vibes = ["хорош", "супер", "класс", "прекрасн"]
negative_vibes = ["плох", "не очень", "так себе"]

# возможные стикеры на ответ пользователю
stickers_positive = ["CAACAgIAAxkBAAEG3DpjnXV_8A6jqV0KeoE9Xo1v-11nTAACHAADwDZPE8GCGtMs_g7hLAQ",
                    # и другие стикеры...  
                    ]

# возможные ответы бота
negative_messages = ["Не переживай, все проходит и это пройдет!",
                    # и любые другие сообщения    
                    ]
positive_messages = ["Я так рад за тебя", 
                    # и любые другие сообщения 
                    ]
neutral_messages  = [ "Я пока не понимаю что это такое, но я буду стараться понять", 
                    # и любые другие сообщения 
                    ]

# приветствие
@dp.message_handler(commands='start')
async def start_command(message):
    
    # Отправляем сообщение пользователю
    await message.answer("Привет! Я виртуальный собеседник: Какая-то тема. Как твои дела?")
    
    # Отправляем приветственный гиф пользователю
    await bot.send_animation(message.chat.id, 'https://i.pinimg.com/originals/7d/9b/1d/7d9b1d662b28cd365b33a01a3d0288e1.gif')
    # С помощью машины состояний будем ожидать ответ пользователя
    await UserState.variable.set()

# обработка отклика на сообщение пользователя
@dp.message_handler(state=UserState.variable)
async def get_state_mood(message, state):

    await state.update_data(variable=message.text)
    answer = await state.get_data()

    value = answer['variable'].strip().lower()
    
    # await state.finish()        # опционально
    #__________________________________________
    # обработка, тело функции
    if sum([value.find(i)!=-1 for i in positive_vibes]):
        await message.answer(random.choice(positive_messages))
        if random.choice([True, False]):
            await bot.send_sticker(message.chat.id, random.choice(stickers_positive))
        else:
            await bot.send_message(message.chat.id, text='☺️')
    elif sum([value.find(i)!=-1 for i in negative_vibes]):
        await message.answer(random.choice(negative_messages))
        await bot.send_sticker(message.chat.id, random.choice(stickers_negative))
        
    else:
        await message.answer(random.choice(neutral_messages))
        await bot.send_sticker(message.chat.id, random.choice(stickers_neutral))
    #__________________________________________
    await message.answer('''Бот что-то отвечает ☺️''')
    # await UserState.field.set() # опционально задаем новое состояние - ожидаем ответ

if __name__ == '__main__':
    executor.start_polling(dp)