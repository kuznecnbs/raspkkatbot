import asyncio
import feedparser
import ssl
import os
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from feedparser.namespaces.mediarss import FeedParserDict

load_dotenv()
RSS_URL = os.environ.get("RSS_URL")
UPDATE_INTERVAL = 1800

router = Router()

parsed_rss = None

if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context


async def scheduled_rss_parser(bot: Bot):
    global parsed_rss
    while True:
        try:
            parsed_rss = feedparser.parse(RSS_URL)
        except Exception as e:
            print(f"Критическая ошибка в планировщике RSS: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)


async def parse_moodle_rss() -> str:
    global parsed_rss

    answer_text = "Последняя замена"

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
    answer_text = await parse_moodle_rss()
    await message.answer(answer_text)
