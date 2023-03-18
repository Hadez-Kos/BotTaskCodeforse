import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

import threading
from parsing.run_parse import main_parse
from config import API_TOKEN
from aiogram.filters import Text
from db.database import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

request = {"theme": "", "solution": ""}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global request
    request = dict()
    kb = [[types.KeyboardButton(text="/help")], [types.KeyboardButton(text="/search")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие"
    )
    await message.answer(
        "Привет меня зовут бот Codic, это команды, которые помогут со мной работать Функции для работы: "
        "\n1) Help - информационная поддержка."
        "\n2) Search - поиск задачи.",
        reply_markup=keyboard,
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    global request
    request = dict()
    await message.answer("""Поиск задачи, бланк помощи.""")


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    kb = [
        [types.KeyboardButton(text="/theme")],
        [types.KeyboardButton(text="/solution")],
        [types.KeyboardButton(text="/back")],
        [types.KeyboardButton(text="/list")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие"
    )
    await message.answer(
        "Поиск задачки по условиям:"
        "\n1) Theme - выбор темы задачи."
        "\n2) Solution - выбор сложности задачи."
        "\n3) List - вывести список задач"
        "\n4) Back - вернуться",
        reply_markup=keyboard,
    )


@dp.message(Command("back"))
async def cmd_search(message: types.Message):
    kb = [[types.KeyboardButton(text="/help")], [types.KeyboardButton(text="/search")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие"
    )
    await message.answer(
        "Оп, вернулись",
        reply_markup=keyboard,
    )


@dp.message(Command("theme"))
async def cmd_search(message: types.Message):
    builder = InlineKeyboardBuilder()
    for theme in await Database().get_data_theme():
        builder.row(
            types.InlineKeyboardButton(
                text=f"{theme}", callback_data=f"call_theme-{theme}"
            )
        )
    await message.answer("Выберите темы задачи:", reply_markup=builder.as_markup())


@dp.message(Command("solution"))
async def cmd_solution(message: types.Message):
    builder = InlineKeyboardBuilder()
    for sol in await Database().get_data_solution(request["theme"]):
        builder.row(
            types.InlineKeyboardButton(
                text=f"{sol}", callback_data=f"call_solution-{sol}"
            )
        )
    await message.answer("Выберите сложность задачи:", reply_markup=builder.as_markup())


@dp.callback_query(Text(startswith="call_"))
async def callbacks_theme(callback: types.CallbackQuery):
    global request
    q = callback.data.split("-")
    if q[0].split("_")[1] == "theme":
        request["theme"] = q[1]
    elif q[0].split("_")[1] == "solution":
        request["solution"] = q[1]
    await callback.answer()


@dp.message(Command("list"))
async def cmd_solution(message: types.Message):
    global request
    response = await Database().get_list_tasks(request)
    if response:
        await message.answer("\n\n".join(response[:10]))
    else:
        await message.answer(
            "К сожалению таких задач нет, только если с комбинированными темами, а это улучшение будет позже"
        )


async def main():
    threading.Timer(3600, await main_parse()).start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
