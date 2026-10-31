import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "bot.db")
TZ = ZoneInfo("Asia/Tashkent")
DEFAULT_SEND_TIME = "07:00"
