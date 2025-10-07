from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

changesButton = KeyboardButton(text="Замены")
keyboard = ReplyKeyboardMarkup(keyboard=[[changesButton]], resize_keyboard=True)
