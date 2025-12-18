from bot.models.user import User
from db.base import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, tg_id: int, username: str = None, full_name: str = None) -> User:
        """Register or get existing user."""
        existing = await self.repo.get_by_tg_id(tg_id)
        if existing:
            return existing
        
        user = User(tg_id=tg_id, username=username, full_name=full_name, language="uz", data={})
        return await self.repo.create(user)

    async def get_user(self, tg_id: int) -> User:
        """Get user by telegram ID."""
        return await self.repo.get_by_tg_id(tg_id)

    async def update_user_language(self, tg_id: int, language: str) -> User:
        """Update user's language preference."""
        user = await self.repo.get_by_tg_id(tg_id)
        if user:
            user.language = language
            return await self.repo.update(user)
        return None

    async def get_all_users(self) -> list[User]:
        """Get all registered users."""
        return await self.repo.get_all_users()
