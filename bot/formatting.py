"""Ob-havo ma'lumotlarini o'zbek tilida chiroyli matnga aylantirish."""
from datetime import date, datetime
from typing import Any

from bot.cities import City
from bot.config import TZ

WEEKDAYS = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
MONTHS = ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul",
          "avgust", "sentabr", "oktabr", "noyabr", "dekabr"]

# WMO ob-havo kodlari -> (emoji, tavsif)
WMO: dict[int, tuple[str, str]] = {
    0: ("☀️", "Ochiq osmon"),
    1: ("🌤", "Asosan ochiq"),
    2: ("🌤", "Qisman bulutli"),
    3: ("☁️", "Bulutli"),
    45: ("🌫", "Tuman"),
    48: ("🌫", "Qirovli tuman"),
    51: ("🌧", "Yengil shivalama yomg'ir"),
    53: ("🌧", "Shivalama yomg'ir"),
    55: ("🌧", "Kuchli shivalama yomg'ir"),
    56: ("🌧", "Muzli shivalama yomg'ir"),
    57: ("🌧", "Kuchli muzli shivalama"),
    61: ("🌧", "Yengil yomg'ir"),
    63: ("🌧", "Yomg'ir"),
    65: ("🌧", "Kuchli yomg'ir"),
    66: ("🌧", "Muzli yomg'ir"),
    67: ("🌧", "Kuchli muzli yomg'ir"),
    71: ("❄️", "Yengil qor"),
    73: ("❄️", "Qor"),
    75: ("❄️", "Kuchli qor"),
    77: ("❄️", "Qor donalari"),
    80: ("🌧", "Yengil jala"),
    81: ("🌧", "Jala"),
    82: ("🌧", "Kuchli jala"),
    85: ("❄️", "Qor yog'ishi"),
    86: ("❄️", "Kuchli qor yog'ishi"),
    95: ("⛈", "Momaqaldiroq"),
    96: ("⛈", "Do'l bilan momaqaldiroq"),
    99: ("⛈", "Kuchli do'l bilan momaqaldiroq"),
}


def describe(code: int | None) -> tuple[str, str]:
    if code is None:
        return "🌡", "Noma'lum"
    return WMO.get(int(code), ("🌡", "Noma'lum"))


def fmt_date(d: date) -> str:
    return f"{d.day}-{MONTHS[d.month - 1]}, {WEEKDAYS[d.weekday()]}"


def t(v: float | None) -> str:
    if v is None:
        return "—"
    r = round(v)
    return f"+{r}°" if r > 0 else f"{r}°"


def num(v: float | None, unit: str = "", digits: int = 0) -> str:
    if v is None:
        return "—"
    return f"{v:.{digits}f}{unit}" if digits else f"{round(v)}{unit}"


def hhmm(iso: str | None) -> str:
    return iso[11:16] if iso else "—"


def _current_hour_precip(data: dict[str, Any]) -> float | None:
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    probs = hourly.get("precipitation_probability", [])
    key = datetime.now(TZ).strftime("%Y-%m-%dT%H:00")
    if key in times:
        return probs[times.index(key)]
    return None


def format_now(city: City, data: dict[str, Any]) -> str:
    cur = data["current"]
    d = data["daily"]
    emoji, desc = describe(cur.get("weather_code"))
    if desc == "Ochiq osmon" and not cur.get("is_day", 1):
        emoji = "🌙"
    now = datetime.now(TZ)
    return (
        f"📍 <b>{city.name}</b> — hozir ({now:%H:%M})\n"
        f"{fmt_date(now.date())}\n\n"
        f"{emoji} <b>{desc}</b>\n"
        f"🌡 Harorat: <b>{t(cur.get('temperature_2m'))}</b>\n"
        f"🤗 His qilinishi: {t(cur.get('apparent_temperature'))}\n"
        f"📊 Bugun: min {t(d['temperature_2m_min'][0])} / max {t(d['temperature_2m_max'][0])}\n"
        f"💧 Namlik: {num(cur.get('relative_humidity_2m'), '%')}\n"
        f"💨 Shamol: {num(cur.get('wind_speed_10m'), ' m/s', 1)}\n"
        f"☔️ Yog'ingarchilik ehtimoli: {num(_current_hour_precip(data), '%')}\n"
        f"🌅 Quyosh chiqishi: {hhmm(d['sunrise'][0])}\n"
        f"🌇 Quyosh botishi: {hhmm(d['sunset'][0])}"
    )


def format_day(city: City, data: dict[str, Any], idx: int, title: str) -> str:
    d = data["daily"]
    day = date.fromisoformat(d["time"][idx])
    emoji, desc = describe(d["weather_code"][idx])
    return (
        f"📍 <b>{city.name}</b> — {title}\n"
        f"{fmt_date(day)}\n\n"
        f"{emoji} <b>{desc}</b>\n"
        f"🌡 Harorat: <b>{t(d['temperature_2m_min'][idx])} … {t(d['temperature_2m_max'][idx])}</b>\n"
        f"🤗 His qilinishi: {t(d['apparent_temperature_min'][idx])} … "
        f"{t(d['apparent_temperature_max'][idx])}\n"
        f"💧 Namlik: {num(d['relative_humidity_2m_mean'][idx], '%')}\n"
        f"💨 Shamol: {num(d['wind_speed_10m_max'][idx], ' m/s', 1)} gacha\n"
        f"☔️ Yog'ingarchilik ehtimoli: {num(d['precipitation_probability_max'][idx], '%')}\n"
        f"🌅 Quyosh chiqishi: {hhmm(d['sunrise'][idx])}\n"
        f"🌇 Quyosh botishi: {hhmm(d['sunset'][idx])}"
    )


def format_week(city: City, data: dict[str, Any]) -> str:
    d = data["daily"]
    lines = [f"📍 <b>{city.name}</b> — 7 kunlik prognoz\n"]
    for i, iso in enumerate(d["time"]):
        day = date.fromisoformat(iso)
        emoji, desc = describe(d["weather_code"][i])
        lines.append(
            f"<b>{day.day}-{MONTHS[day.month - 1]}, {WEEKDAYS[day.weekday()]}</b>\n"
            f"{emoji} {desc}\n"
            f"🌡 {t(d['temperature_2m_min'][i])} … {t(d['temperature_2m_max'][i])} "
            f"(his: {t(d['apparent_temperature_min'][i])} … {t(d['apparent_temperature_max'][i])})\n"
            f"💧 {num(d['relative_humidity_2m_mean'][i], '%')}  "
            f"💨 {num(d['wind_speed_10m_max'][i], ' m/s', 1)}  "
            f"☔️ {num(d['precipitation_probability_max'][i], '%')}\n"
            f"🌅 {hhmm(d['sunrise'][i])}  🌇 {hhmm(d['sunset'][i])}\n"
        )
    return "\n".join(lines)


PERIODS = {
    "now": "Hozir",
    "today": "Bugun",
    "tomorrow": "Ertaga",
    "week": "7 kunlik",
}


def format_period(city: City, data: dict[str, Any], period: str) -> str:
    if period == "now":
        return format_now(city, data)
    if period == "today":
        return format_day(city, data, 0, "bugun")
    if period == "tomorrow":
        return format_day(city, data, 1, "ertaga")
    return format_week(city, data)

