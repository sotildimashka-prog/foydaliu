from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.cities import CITIES
from bot.formatting import PERIODS

WEATHER_BTN = "🌤 Ob-havo"
SUBSCRIBE_BTN = "🔔 Obuna"
SETTINGS_BTN = "⏰ Vaqtni o'zgartirish"


class CityCB(CallbackData, prefix="city"):
    action: str  # "w" — ob-havo ko'rish, "sub" — obuna
    city: str


class PeriodCB(CallbackData, prefix="per"):
    city: str
    period: str


class NavCB(CallbackData, prefix="nav"):
    to: str  # "cities"


class TimeCB(CallbackData, prefix="time"):
    value: str  # "0700" ko'rinishida yoki "custom"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=WEATHER_BTN)],
            [KeyboardButton(text=SUBSCRIBE_BTN), KeyboardButton(text=SETTINGS_BTN)],
        ],
        resize_keyboard=True,
    )


def cities_kb(action: str = "w") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in CITIES.values():
        kb.button(text=c.name, callback_data=CityCB(action=action, city=c.key))
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


TIME_PRESETS = ["05:00", "05:30", "06:00", "06:30", "07:00", "07:30",
                "08:00", "08:30", "09:00", "10:00", "12:00", "20:00"]


def times_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for tm in TIME_PRESETS:
        kb.button(text=tm, callback_data=TimeCB(value=tm.replace(":", "")))
    kb.button(text="✍️ Boshqa vaqt", callback_data=TimeCB(value="custom"))
    kb.adjust(4, 4, 4, 1)
    return kb.as_markup()
