import asyncio
import os
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
from handlers import general, moodle_rss
from handlers.moodle_rss import scheduled_rss_parser

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(moodle_rss.router)
dp.include_router(general.router)


async def on_startup(bot: Bot):
    print("Бот запущен. Запускаю планировщик парсинга...")
    asyncio.create_task(scheduled_rss_parser(bot))


async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен. Наконец-то тишина.")
