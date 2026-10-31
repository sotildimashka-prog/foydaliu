"""Har daqiqada obunalarni tekshirib, vaqti kelganlarga ob-havo yuboradi."""
import asyncio
import logging
from datetime import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

from bot import db
from bot.cities import CITIES
from bot.config import TZ
from bot.formatting import format_daily_message
from bot.weather import WeatherError, get_forecast

log = logging.getLogger(__name__)


async def send_due(bot: Bot, now: datetime) -> None:
    today = now.date().isoformat()
    subs = await db.due_subscriptions(now.strftime("%H:%M"), today)
    for user_id, chat_id, city_key in subs:
        city = CITIES.get(city_key)
        if not city:
            continue
        try:
            data = await get_forecast(city)
            text = format_daily_message(city, data)
            try:
                await bot.send_message(chat_id, text)
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                await bot.send_message(chat_id, text)
            await db.mark_sent(user_id, today)
        except TelegramForbiddenError:
            log.info("User %s blocked the bot, removing subscription", user_id)
            await db.delete_subscription(user_id)
        except WeatherError as e:
            log.warning("Weather fetch failed for %s: %s", city_key, e)
        except Exception:
            log.exception("Failed to send daily weather to %s", user_id)
        await asyncio.sleep(0.05)  # Telegram limitlariga rioya qilish


async def run_scheduler(bot: Bot) -> None:
    log.info("Scheduler started")
    while True:
        now = datetime.now(TZ)
        try:
            await send_due(bot, now)
        except Exception:
            log.exception("Scheduler tick failed")
        # keyingi daqiqa boshigacha kutish
        now = datetime.now(TZ)
        await asyncio.sleep(60 - now.second - now.microsecond / 1e6 + 0.5)
