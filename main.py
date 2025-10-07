import asyncio
import os
from aiogram.fsm.storage.base import KeyBuilder
import feedparser
import ssl
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

load_dotenv()

RSS_URL = os.environ.get("RSS_URL")
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

changesButton = KeyboardButton(text="Замены")
keyboard = ReplyKeyboardMarkup(keyboard=[[changesButton]], resize_keyboard=True)


if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context


async def parse_moodle_rss(url) -> str:
    parsed_rss = feedparser.parse(url)

    if parsed_rss.get("status") not in (200, 301, 302, 303):
        return f"Ошибка при загрузке: Статус {parsed_rss.get('status', 'неизвестен')}."

    answer_text = parsed_rss.feed.title

    if not parsed_rss.entries:
        answer_text += "\n Записи не найдены"
        return answer_text

    for i, entry in enumerate(parsed_rss.entries, 1):
        title = entry.get("title", "Нет заголовка")
        link = entry.get("link", "Нет ссылки")
        published = entry.get("published", "Дата неизвестна")

        answer_text += f"\n📝 {title}\n📅 {published}\n➡️ {link}"
        return answer_text


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Приветствую, {message.from_user.full_name}! Я бот с заменами",
        reply_markup=keyboard,
    )


@router.message(F.text == "Замены")
@router.message(Command("changes"))
async def get_changes(message: types.Message) -> None:
    await bot.send_chat_action(message.chat.id, "typing")
    answer_text = await parse_moodle_rss(RSS_URL)
    await message.answer(answer_text)


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(
        "Я не знаю такой команды. Не трать мое время.", reply_markup=keyboard
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен. Наконец-то тишина.")
