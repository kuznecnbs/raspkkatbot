from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards import keyboard

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Приветствую, {message.from_user.full_name}! Я бот с заменами",
        reply_markup=keyboard,
    )


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(
        "Я не знаю такой команды. Не трать мое время.", reply_markup=keyboard
    )
