# Ob-havo boti (aiogram 3.x)

O'zbekiston shaharlari uchun kunlik ob-havo boti. Ma'lumot manbai — [Open-Meteo](https://open-meteo.com) (bepul, API kalit kerak emas).

## Imkoniyatlar
- 🏙 13 ta shahar → 📅 davr tanlash (Hozir | Bugun | Ertaga | 7 kunlik)
- Harorat (min/max), his qilinishi, namlik, shamol, yog'ingarchilik ehtimoli, quyosh chiqishi/botishi
- Ob-havo holatiga mos emoji: ☀️ 🌤 ☁️ 🌧 ❄️ ⛈ 🌫

## Buyruqlar
| Buyruq | Vazifasi |
|---|---|
| `/weather` | Ob-havoni ko'rish (shahar → davr) |
| `/help` | Yordam |

## Ishga tushirish
```bash
pip install -r requirements.txt
cp .env.example .env      # BOT_TOKEN ni yozing
python -m bot
```

## Tuzilma
```
bot/
  __main__.py        # kirish nuqtasi
  config.py          # sozlamalar (.env)
  cities.py          # shaharlar va koordinatalar
  weather.py         # Open-Meteo mijozi (10 daqiqalik kesh)
  formatting.py      # o'zbekcha matnlar, emoji
  keyboards.py       # inline tugmalar
  handlers/          # common, weather
```
