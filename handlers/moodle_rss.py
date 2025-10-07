import feedparser
import ssl
import os
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
RSS_URL = os.environ.get("RSS_URL")

router = Router()


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


@router.message(F.text == "Замены")
@router.message(Command("changes"))
async def get_changes(message: types.Message) -> None:
    await message.bot.send_chat_action(message.chat.id, "typing")
    answer_text = await parse_moodle_rss(RSS_URL)
    await message.answer(answer_text)
