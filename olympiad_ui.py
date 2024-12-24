import asyncio
import locale
import pymorphy3
import logging
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = 'VstavteSvoiTOKEN'
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Всемирный календарь")
    keyboard.button(text="Православный календарь")
    await message.answer("Выберите календарь:", reply_markup=keyboard.as_markup(resize_keyboard=True))


@dp.message(F.text == "Всемирный календарь")
async def world_calendar(message: Message):
    today = datetime.now().strftime('%d %B')
    ch, sl = today.split(' ')

    morph = pymorphy3.MorphAnalyzer()
    slovo = morph.parse(sl)[1]
    gent = slovo.inflect({'gent'}).word
    holiday = holidays['world'].get(ch + ' ' + gent, "Нет праздника на сегодня.")
    await message.answer(f"Сегодня: {holiday}")


@dp.message(F.text == "Православный календарь")
async def orthodox_calendar(message: Message):
    today = datetime.now().strftime('%d %B')
    ch, sl = today.split(' ')

    morph = pymorphy3.MorphAnalyzer()
    slovo = morph.parse(sl)[1]
    gent = slovo.inflect({'gent'}).word
    holiday = holidays['orthodox'].get(ch + ' ' + gent, "Нет праздника на сегодня.")
    await message.answer(f"Сегодня: {holiday}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
