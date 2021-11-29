
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import token

import consoli_parser as c_parser

client = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(client)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def welcom(message: types.Message):
    keboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Консоли']
    keboard.add(*buttons)
    await message.answer('Что спарсим на этот раз?', reply_markup=keboard)


@dp.message_handler(Text('Консоли'))
async def with_cetchup(message: types.Message):
    await message.reply('Пожалуйста подождите...',
                        reply_markup=types.ReplyKeyboardRemove())
    for product in c_parser.parse()['products']:
        message2 = f"""Вы можете купить <a href="{product['link']}">{product['title']}</a>\nпо цене {product['price']}"""
        await message.answer(message2, disable_notification=True)

    welcom(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
