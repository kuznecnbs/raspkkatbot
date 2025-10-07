from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards import keyboard
from services.db_service import (
    get_all_notificated_users,
    turn_on_notifications,
    turn_off_notifications,
)

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Приветствую, {message.from_user.full_name}! Я бот с заменами",
        reply_markup=keyboard,
    )


@router.message(Command("turn_on_notifications"))
async def turn_on_notifications_handler(message: types.Message) -> None:
    await turn_on_notifications(message.chat.id)
    await message.answer("Уведомления о заменах включены")


@router.message(Command("turn_off_notifications"))
async def turn_off_notifications_handler(message: types.Message) -> None:
    await turn_off_notifications(message.chat.id)
    await message.answer("Уведомления о заменах выключены")


@router.message(Command("get_users"))
async def get_users_handler(message: types.Message) -> None:
    print(await get_all_notificated_users())


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(
        "Я не знаю такой команды. Не трать мое время.", reply_markup=keyboard
    )
