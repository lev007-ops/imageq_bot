import requests
import json

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time



API_TOKEN = 'token'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)






@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #print(message.as_json())
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    
    
    

    
    await message.answer("@image_quality_bot приветствует вас!")
    await message.answer('''Бот разработан @Levman5

Бот умеет улучшать качество картинок. Для начала работы воспользуйтесь командой:  /new_image''')
    


@dp.message_handler(commands=['new_image'])
async def new_image(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Я соглашаюсь", callback_data="content"))
    await message.answer("Используя бота, вы соглашаетесь с тем, что автор бота не имеет никакого отношение к контенту преобразованному в боте.", reply_markup=keyboard) 
    

    #await message.answer("Используя бота вы соглашаетесь с тем что автор бота не имеет никакого отношение к контенту преобразованному в боте в боте.", reply_markup=inline_kb1)


@dp.callback_query_handler(text="content")
async def send_content(call: types.CallbackQuery):
    await call.message.answer("Вы согласились с условиями")
    await call.message.answer("Отправьте мне фотографию")


    


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await message.answer("Фото получено")
    await message.answer("Обработка фото")
    #await message.photo[-1].download('test.jpg')
    file = await bot.get_file(message.photo[-1].file_id) # message - тип того что вам пришло.
    url = f'https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}'
    #print(url)
    r = requests.post(
    "https://api.deepai.org/api/waifu2x",
    data={
        'image': url,
    },
    headers={'api-key': 'e3171afd-b524-4df1-8790-695344af0ff9'}
)
    #print(r.json())

    i = r.json()


    #print(i)
    i = i['output_url']


    




    
    #print(i)

    file_name = "image.png"

    img_data = requests.get(i).content
    with open(file_name, 'wb') as handler:
        handler.write(img_data)
    #print("Файл " + file_name + " успешно сохранён!")
    await message.answer(i)
    



    
    


@dp.message_handler()
async def json(message: types.Message):
#async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    pass







executor.start_polling(dp, skip_updates=True)
