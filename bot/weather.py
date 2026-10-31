"""Open-Meteo API mijozi (bepul, API kalit talab qilmaydi)."""
import time
from typing import Any

import aiohttp

from bot.cities import City

API_URL = "https://api.open-meteo.com/v1/forecast"
CACHE_TTL = 600  # 10 daqiqa

_cache: dict[str, tuple[float, dict[str, Any]]] = {}


class WeatherError(Exception):
    pass


async def get_forecast(city: City) -> dict[str, Any]:
    cached = _cache.get(city.key)
    if cached and time.monotonic() - cached[0] < CACHE_TTL:
        return cached[1]

    params = {
        "latitude": city.lat,
        "longitude": city.lon,
        "timezone": "Asia/Tashkent",
        "forecast_days": 7,
        "wind_speed_unit": "ms",
        "current": ",".join([
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "weather_code", "wind_speed_10m", "is_day",
        ]),
        "hourly": "precipitation_probability",
        "daily": ",".join([
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "apparent_temperature_max", "apparent_temperature_min",
            "relative_humidity_2m_mean", "wind_speed_10m_max",
            "precipitation_probability_max", "sunrise", "sunset",
        ]),
    }
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL, params=params) as resp:
                if resp.status != 200:
                    raise WeatherError(f"HTTP {resp.status}")
                data = await resp.json()
    except (aiohttp.ClientError, TimeoutError) as e:
        raise WeatherError(str(e)) from e

    _cache[city.key] = (time.monotonic(), data)
    return data
