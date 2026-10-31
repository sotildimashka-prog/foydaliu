import re

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot import db
from bot.cities import CITIES
from bot.config import DEFAULT_SEND_TIME
from bot.keyboards import SETTINGS_BTN, SUBSCRIBE_BTN, CityCB, TimeCB, cities_kb, times_kb

router = Router()

TIME_RE = re.compile(r"^([01]?\d|2[0-3])[:.]([0-5]\d)$")


class SetTime(StatesGroup):
    waiting = State()


def parse_time(text: str) -> str | None:
    m = TIME_RE.match(text.strip())
    if not m:
        return None
    return f"{int(m.group(1)):02d}:{m.group(2)}"


# ---------- /subscribe ----------

@router.message(Command("subscribe"))
@router.message(F.text == SUBSCRIBE_BTN)
async def cmd_subscribe(message: Message) -> None:
    await message.answer(
        "🔔 <b>Kunlik ob-havo obunasi</b>\n\n"
        "Har kuni qaysi shahar ob-havosini olishni xohlaysiz?",
        reply_markup=cities_kb("sub"),
    )


@router.callback_query(CityCB.filter(F.action == "sub"))
async def on_subscribe_city(cq: CallbackQuery, callback_data: CityCB) -> None:
    city = CITIES.get(callback_data.city)
    if not city:
        await cq.answer("Shahar topilmadi", show_alert=True)
        return
    send_time = await db.upsert_subscription(
        cq.from_user.id, cq.message.chat.id, city.key, DEFAULT_SEND_TIME
    )
    await cq.message.edit_text(
        f"✅ Obuna faollashtirildi!\n\n"
        f"📍 Shahar: <b>{city.name}</b>\n"
        f"⏰ Vaqt: <b>{send_time}</b> (Toshkent vaqti)\n\n"
        f"Vaqtni o'zgartirish: /settime\n"
        f"Bekor qilish: /unsubscribe"
    )
    await cq.answer("Obuna bo'ldingiz ✅")


# ---------- /unsubscribe ----------

@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message) -> None:
    if await db.delete_subscription(message.from_user.id):
        await message.answer("🔕 Obuna bekor qilindi. Qayta obuna bo'lish: /subscribe")
    else:
        await message.answer("Sizda faol obuna yo'q. Obuna bo'lish: /subscribe")


# ---------- /mysub ----------

@router.message(Command("mysub"))
async def cmd_mysub(message: Message) -> None:
    sub = await db.get_subscription(message.from_user.id)
    if not sub:
        await message.answer("Sizda faol obuna yo'q. Obuna bo'lish: /subscribe")
        return
    city_key, send_time = sub
    city = CITIES.get(city_key)
    await message.answer(
        f"📋 <b>Obunangiz</b>\n\n"
        f"📍 Shahar: <b>{city.name if city else city_key}</b>\n"
        f"⏰ Vaqt: <b>{send_time}</b> (Toshkent vaqti)"
    )


# ---------- /settime ----------

@router.message(Command("settime"))
@router.message(F.text == SETTINGS_BTN)
async def cmd_settime(message: Message, state: FSMContext, command: CommandObject | None = None) -> None:
    sub = await db.get_subscription(message.from_user.id)
    if not sub:
        await message.answer("Avval obuna bo'ling: /subscribe")
        return

    # /settime 06:30 ko'rinishida ham ishlaydi
    if command and command.args:
        tm = parse_time(command.args)
        if tm:
            await _apply_time(message, state, tm)
            return
        await message.answer("❌ Noto'g'ri format. Masalan: <code>/settime 06:30</code>")
        return

    await message.answer(
        f"⏰ Hozirgi vaqt: <b>{sub[1]}</b>\n\nYangi vaqtni tanlang (Toshkent vaqti):",
        reply_markup=times_kb(),
    )


@router.callback_query(TimeCB.filter(F.value == "custom"))
async def on_custom_time(cq: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SetTime.waiting)
    await cq.message.edit_text(
        "✍️ Vaqtni <b>SS:DD</b> formatida yozing.\nMasalan: <code>06:45</code>\n\nBekor qilish: /cancel"
    )
    await cq.answer()


@router.callback_query(TimeCB.filter())
async def on_preset_time(cq: CallbackQuery, callback_data: TimeCB, state: FSMContext) -> None:
    v = callback_data.value
    tm = f"{v[:2]}:{v[2:]}"
    if await db.set_time(cq.from_user.id, tm):
        await state.clear()
        await cq.message.edit_text(f"✅ Kunlik xabar vaqti <b>{tm}</b> ga o'rnatildi.")
        await cq.answer()
    else:
        await cq.answer("Avval obuna bo'ling: /subscribe", show_alert=True)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Bekor qilindi.")


@router.message(SetTime.waiting, F.text)
async def on_time_text(message: Message, state: FSMContext) -> None:
    tm = parse_time(message.text)
    if not tm:
        await message.answer("❌ Noto'g'ri format. Masalan: <code>07:15</code>\nBekor qilish: /cancel")
        return
    await _apply_time(message, state, tm)


async def _apply_time(message: Message, state: FSMContext, tm: str) -> None:
    await state.clear()
    if await db.set_time(message.from_user.id, tm):
        await message.answer(f"✅ Kunlik xabar vaqti <b>{tm}</b> ga o'rnatildi.")
    else:
        await message.answer("Avval obuna bo'ling: /subscribe")
