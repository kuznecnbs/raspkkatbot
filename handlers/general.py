from typing_extensions import Text
from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from services.moodle_rss import get_latest_change
from keyboards import keyboard_menu_main, keyboard_menu_options, keyboard_menu_changes
from services.db_service import (
    get_all_notificated_users,
    turn_on_notifications,
    turn_off_notifications,
    get_user_notification_status,
)

router = Router()


# callback handlers


@router.callback_query(F.data == "menu_main")
async def main_menu_callback_handler(callback: types.CallbackQuery) -> None:
    await callback.answer("📋Главное меню")
    await callback.message.edit_text("📋Главное меню", reply_markup=keyboard_menu_main)


@router.callback_query(F.data == "menu_options")
async def options_menu_callback_handler(callback: types.CallbackQuery) -> None:
    await callback.answer("⚙️Настройки")
    if await get_user_notification_status(callback.message.chat.id):
        notification_status = "1"
    else:
        notification_status = "0"
    menu_options_text = str(
        f"⚙️Настройки\n------------------\n📣Уведомления = {notification_status}"
    )
    await callback.message.edit_text(
        menu_options_text,
        reply_markup=keyboard_menu_options,
    )


@router.callback_query(F.data == "turn_on_notifications")
async def turn_on_notifications_handler(callback: types.CallbackQuery) -> None:
    await turn_on_notifications(callback.message.chat.id)
    await callback.answer("🔔Уведомления включены")

    if await get_user_notification_status(callback.message.chat.id):
        notification_status = "1"
    else:
        notification_status = "0"
    menu_options_text = str(
        f"⚙️Настройки\n------------------\n📣Уведомления = {notification_status}"
    )
    try:
        await callback.message.edit_text(
            menu_options_text,
            reply_markup=keyboard_menu_options,
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e


@router.callback_query(F.data == "turn_off_notifications")
async def turn_off_notifications_handler(callback: types.CallbackQuery) -> None:
    await turn_off_notifications(callback.message.chat.id)
    await callback.answer("🔕Уведомления выключены")

    if await get_user_notification_status(callback.message.chat.id):
        notification_status = "1"
    else:
        notification_status = "0"
    menu_options_text = str(
        f"⚙️Настройки\n------------------\n📣Уведомления = {notification_status}"
    )
    try:
        await callback.message.edit_text(
            menu_options_text,
            reply_markup=keyboard_menu_options,
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e


# 123132


@router.callback_query(F.data == "menu_changes")
async def options_menu_callback_handler(callback: types.CallbackQuery) -> None:
    await callback.answer("Замены")
    answer_text = await get_latest_change()
    try:
        await callback.message.edit_text(
            answer_text, reply_markup=keyboard_menu_changes
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise e


# command handlers


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Приветствую, {message.from_user.full_name}! Я бот с заменами",
        reply_markup=None,
    )
    await message.answer("📋Главное меню", reply_markup=keyboard_menu_main)


@router.message(Command("menu"))
async def command_start_handler(message: types.Message) -> None:
    await message.answer("📋Главное меню", reply_markup=keyboard_menu_main)


@router.message(Command("get_users"))
async def command_get_users_handler(message: types.Message) -> None:
    print(await get_all_notificated_users())


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer("Я не знаю такой команды. \n/menu - чтобы открыть меню.")
