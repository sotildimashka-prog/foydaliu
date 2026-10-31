# Ob-havo boti (aiogram 3.x)

O'zbekiston shaharlari uchun kunlik ob-havo boti. Ma'lumot manbai — [Open-Meteo](https://open-meteo.com) (bepul, API kalit kerak emas).

## Imkoniyatlar
- 🏙 13 ta shahar → 📅 davr tanlash (Hozir | Bugun | Ertaga | 7 kunlik)
- Harorat (min/max), his qilinishi, namlik, shamol, yog'ingarchilik ehtimoli, quyosh chiqishi/botishi
- Ob-havo holatiga mos emoji: ☀️ 🌤 ☁️ 🌧 ❄️ ⛈ 🌫
- Kunlik avtomatik xabar (Asia/Tashkent, standart 07:00)

## Buyruqlar
| Buyruq | Vazifasi |
|---|---|
| `/weather` | Ob-havoni ko'rish |
| `/subscribe` | Shaharni tanlab kunlik obuna |
| `/settime` | Xabar vaqtini o'zgartirish (`/settime 06:30` ham ishlaydi) |
| `/mysub` | Obuna holati |
| `/unsubscribe` | Obunani bekor qilish |

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
  db.py              # SQLite obunalar
  scheduler.py       # kunlik xabar yuboruvchi
  handlers/          # common, weather, subscription
```
