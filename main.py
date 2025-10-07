import asyncio
import os
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
from handlers import general, moodle_rss

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(moodle_rss.router)
dp.include_router(general.router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен. Наконец-то тишина.")
