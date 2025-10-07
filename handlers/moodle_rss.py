import asyncio
import feedparser
import ssl
import os
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from feedparser.namespaces.mediarss import FeedParserDict
from services.db_service import get_all_notificated_users

load_dotenv()
RSS_URL = os.environ.get("RSS_URL")
UPDATE_INTERVAL = 1800

router = Router()

parsed_rss = None
new_parsed_rss = None

if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context


async def send_notification_to_users(bot: Bot, message_text: str):
    user_ids = await get_all_notificated_users()

    if not user_ids:
        print("Рассылка: активных подписчиков не найдено.")
        return

    print(f"Рассылка: Найдено {len(user_ids)} активных получателей.")

    for chat_id in user_ids:
        try:
            await bot.send_message(
                chat_id=chat_id, text=message_text, parse_mode="Markdown"
            )
            await asyncio.sleep(0.05)

        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {chat_id}: {e}")
    print("Уведомления отправлены")


async def scheduled_rss_parser(bot: Bot):
    global parsed_rss
    global new_parsed_rss
    parsed_rss = feedparser.parse(RSS_URL)
    while True:
        try:
            new_parsed_rss = feedparser.parse(RSS_URL)
            entry = parsed_rss.entries[0]
            new_entry = new_parsed_rss.entries[0]
            entry_link = entry.get("link")
            new_entry_link = new_entry.get("link")
            if entry_link != new_entry_link:
                parsed_rss = new_parsed_rss
                message_text = await get_latest_change()
                await send_notification_to_users(bot, message_text)

        except Exception as e:
            print(f"Критическая ошибка в планировщике RSS: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)


async def get_latest_change() -> str:
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
    answer_text = await get_latest_change()
    await message.answer(answer_text)
