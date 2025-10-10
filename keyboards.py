from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from services.db_service import turn_off_notifications, turn_on_notifications

button_menu_changes = InlineKeyboardButton(text="Замены", callback_data="menu_changes")
button_menu_options = InlineKeyboardButton(
    text="Настройки", callback_data="menu_options"
)
button_back_to_main_menu = InlineKeyboardButton(text="Назад", callback_data="menu_main")
button_turn_on_notification = InlineKeyboardButton(
    text="🔔Включить уведомления", callback_data="turn_on_notifications"
)
button_turn_off_notification = InlineKeyboardButton(
    text="🔕Выключить уведомления", callback_data="turn_off_notifications"
)
button_update_changes = InlineKeyboardButton(
    text="🔄Обновить", callback_data="menu_changes"
)


keyboard_menu_main = InlineKeyboardMarkup(
    inline_keyboard=[[button_menu_changes], [button_menu_options]]
)
keyboard_menu_options = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_turn_on_notification, button_turn_off_notification],
        [button_back_to_main_menu],
    ]
)
keyboard_menu_changes = InlineKeyboardMarkup(
    inline_keyboard=[[button_update_changes], [button_back_to_main_menu]]
)
