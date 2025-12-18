import aiosqlite
import json
from typing import Optional
from bot.models.user import User
from db.base import UserRepository


class SqliteUserRepo(UserRepository):
    def __init__(self, database_path: str):
        # database_path: path to sqlite file, e.g. './data.db'
        self._db_path = database_path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self) -> None:
        self._conn = await aiosqlite.connect(self._db_path)
        # store rows as text for JSON column
        await self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                full_name TEXT,
                language TEXT DEFAULT 'uz',
                data TEXT
            )
            """
        )
        # Add language column if it doesn't exist (for migration)
        try:
            await self._conn.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")
        except Exception:
            # Column already exists
            pass
        await self._conn.commit()

    async def _row_to_user(self, row) -> Optional[User]:
        if not row:
            return None
        id_, tg_id, username, full_name, language, data_text = row
        data = json.loads(data_text) if data_text else {}
        return User(id=id_, tg_id=tg_id, username=username, full_name=full_name, language=language or "uz", data=data)

    async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
        async with self._conn.execute("SELECT id,tg_id,username,full_name,language,data FROM users WHERE tg_id = ?", (tg_id,)) as cur:
            row = await cur.fetchone()
            return await self._row_to_user(row)

    async def create(self, user: User) -> User:
        data_text = json.dumps(user.data or {})
        async with self._conn.execute(
            "INSERT INTO users (tg_id, username, full_name, language, data) VALUES (?, ?, ?, ?, ?)",
            (user.tg_id, user.username, user.full_name, user.language, data_text),
        ) as cur:
            await self._conn.commit()
            user.id = cur.lastrowid
            return user

    async def update(self, user: User) -> User:
        data_text = json.dumps(user.data or {})
        await self._conn.execute(
            "UPDATE users SET username = ?, full_name = ?, language = ?, data = ? WHERE tg_id = ?",
            (user.username, user.full_name, user.language, data_text, user.tg_id),
        )
        await self._conn.commit()
        return user

    async def get_all_users(self) -> list[User]:
        """Get all users from the database."""
        async with self._conn.execute("SELECT id,tg_id,username,full_name,language,data FROM users") as cur:
            rows = await cur.fetchall()
            return [await self._row_to_user(row) for row in rows]

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None
