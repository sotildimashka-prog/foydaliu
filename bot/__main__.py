import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.config import BOT_TOKEN
from bot.handlers import common, weather

COMMANDS = [
    BotCommand(command="start", description="Botni ishga tushirish"),
    BotCommand(command="weather", description="Ob-havoni ko'rish"),
    BotCommand(command="help", description="Yordam"),
]


async def main() -> None:
    if not BOT_TOKEN:
        sys.exit("BOT_TOKEN topilmadi. .env fayliga BOT_TOKEN=... yozing.")

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(common.router, weather.router)

    await bot.set_my_commands(COMMANDS)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(main())
