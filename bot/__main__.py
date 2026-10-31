import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.config import BOT_TOKEN
from bot.db import init_db
from bot.handlers import common, subscription, weather
from bot.scheduler import run_scheduler

COMMANDS = [
    BotCommand(command="start", description="Botni ishga tushirish"),
    BotCommand(command="weather", description="Ob-havoni ko'rish"),
    BotCommand(command="subscribe", description="Kunlik ob-havoga obuna"),
    BotCommand(command="settime", description="Xabar vaqtini o'zgartirish"),
    BotCommand(command="mysub", description="Obuna holati"),
    BotCommand(command="unsubscribe", description="Obunani bekor qilish"),
    BotCommand(command="help", description="Yordam"),
]


async def main() -> None:
    if not BOT_TOKEN:
        sys.exit("BOT_TOKEN topilmadi. .env fayliga BOT_TOKEN=... yozing.")

    await init_db()
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(common.router, subscription.router, weather.router)

    await bot.set_my_commands(COMMANDS)
    scheduler_task = asyncio.create_task(run_scheduler(bot))
    try:
        await dp.start_polling(bot)
    finally:
        scheduler_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(main())
