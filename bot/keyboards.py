from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.cities import CITIES
from bot.formatting import PERIODS

WEATHER_BTN = "🌤 Ob-havo"


class CityCB(CallbackData, prefix="city"):
    city: str


class PeriodCB(CallbackData, prefix="per"):
    city: str
    period: str


class NavCB(CallbackData, prefix="nav"):
    to: str  # "cities"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=WEATHER_BTN)],
        ],
        resize_keyboard=True,
    )


def cities_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in CITIES.values():
        kb.button(text=c.name, callback_data=CityCB(city=c.key))
    kb.adjust(3)
    return kb.as_markup()


def periods_kb(city: str, current: str | None = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, label in PERIODS.items():
        text = f"• {label} •" if key == current else label
        kb.button(text=text, callback_data=PeriodCB(city=city, period=key))
    kb.button(text="🏙 Shaharlar", callback_data=NavCB(to="cities"))
    kb.adjust(4, 1)
    return kb.as_markup()

