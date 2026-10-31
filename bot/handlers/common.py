from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.keyboards import main_menu

router = Router()

HELP = (
    "🤖 <b>Ob-havo boti</b>\n\n"
    "🌤 /weather — ob-havoni ko'rish\n"
    "Avval shaharni, keyin davrni tanlang: Hozir | Bugun | Ertaga | 7 kunlik\n\n"
    "❓ /help — yordam"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name if message.from_user else ""
    await message.answer(
        f"Assalomu alaykum, {name}! 👋\n\n" + HELP,
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP, reply_markup=main_menu())
