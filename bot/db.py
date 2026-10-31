import aiosqlite

from bot.config import DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS subscriptions (
    user_id   INTEGER PRIMARY KEY,
    chat_id   INTEGER NOT NULL,
    city      TEXT    NOT NULL,
    send_time TEXT    NOT NULL DEFAULT '07:00',
    last_sent TEXT
);
CREATE INDEX IF NOT EXISTS idx_sub_time ON subscriptions(send_time);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(_SCHEMA)
        await db.commit()


async def upsert_subscription(user_id: int, chat_id: int, city: str, default_time: str) -> str:
    """Obunani yaratadi yoki shaharni yangilaydi. Joriy yuborish vaqtini qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO subscriptions (user_id, chat_id, city, send_time)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET city=excluded.city, chat_id=excluded.chat_id""",
            (user_id, chat_id, city, default_time),
        )
        await db.commit()
        cur = await db.execute("SELECT send_time FROM subscriptions WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0]


async def get_subscription(user_id: int) -> tuple[str, str] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT city, send_time FROM subscriptions WHERE user_id=?", (user_id,)
        )
        row = await cur.fetchone()
        return (row[0], row[1]) if row else None


async def delete_subscription(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("DELETE FROM subscriptions WHERE user_id=?", (user_id,))
        await db.commit()
        return cur.rowcount > 0


async def set_time(user_id: int, send_time: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "UPDATE subscriptions SET send_time=? WHERE user_id=?", (send_time, user_id)
        )
        await db.commit()
        return cur.rowcount > 0


async def due_subscriptions(send_time: str, today: str) -> list[tuple[int, int, str]]:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """SELECT user_id, chat_id, city FROM subscriptions
               WHERE send_time=? AND (last_sent IS NULL OR last_sent<>?)""",
            (send_time, today),
        )
        return [tuple(r) for r in await cur.fetchall()]


async def mark_sent(user_id: int, today: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE subscriptions SET last_sent=? WHERE user_id=?", (today, user_id))
        await db.commit()
