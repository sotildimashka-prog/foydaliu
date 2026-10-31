import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.cities import CITIES
from bot.formatting import format_period
from bot.keyboards import WEATHER_BTN, CityCB, NavCB, PeriodCB, cities_kb, periods_kb
from bot.weather import WeatherError, get_forecast

router = Router()
log = logging.getLogger(__name__)

CHOOSE_CITY = "🏙 <b>Shaharlar</b>\n\nShaharni tanlang:"


@router.message(Command("weather"))
@router.message(F.text == WEATHER_BTN)
async def cmd_weather(message: Message) -> None:
    await message.answer(CHOOSE_CITY, reply_markup=cities_kb("w"))


@router.callback_query(NavCB.filter(F.to == "cities"))
async def back_to_cities(cq: CallbackQuery) -> None:
    await _safe_edit(cq, CHOOSE_CITY, cities_kb("w"))
    await cq.answer()


@router.callback_query(CityCB.filter(F.action == "w"))
async def on_city(cq: CallbackQuery, callback_data: CityCB) -> None:
    city = CITIES.get(callback_data.city)
    if not city:
        await cq.answer("Shahar topilmadi", show_alert=True)
        return
    await _safe_edit(
        cq,
        f"📍 <b>{city.name}</b>\n\n📅 <b>Davr</b>ni tanlang:",
        periods_kb(city.key),
    )
    await cq.answer()


@router.callback_query(PeriodCB.filter())
async def on_period(cq: CallbackQuery, callback_data: PeriodCB) -> None:
    city = CITIES.get(callback_data.city)
    if not city:
        await cq.answer("Shahar topilmadi", show_alert=True)
        return
    await cq.answer("⏳ Yuklanmoqda...")
    try:
        data = await get_forecast(city)
        text = format_period(city, data, callback_data.period)
    except WeatherError as e:
        log.warning("Weather error for %s: %s", city.key, e)
        text = "⚠️ Ob-havo ma'lumotini olishda xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring."
    await _safe_edit(cq, text, periods_kb(city.key, callback_data.period))


async def _safe_edit(cq: CallbackQuery, text: str, markup) -> None:
    try:
        await cq.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest as e:
        # "message is not modified" — bir xil tugma qayta bosilganda
        if "not modified" not in str(e):
            raise
