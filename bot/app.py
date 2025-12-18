from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import settings
from bot.services.user_service import UserService
from bot.handlers import start, broadcast
from db import get_user_repo


async def create_bot_and_dispatcher(user_repo):
    """Initialize bot, dispatcher, and handlers."""
    storage = MemoryStorage()
    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher(storage=storage)

    # Create user service
    user_service = UserService(user_repo)

    # Setup handlers
    start_router = await start.setup_start_handler(user_service)
    broadcast_router = await broadcast.setup_broadcast_handler(user_service)

    dp.include_router(start_router)
    dp.include_router(broadcast_router)

    return bot, dp


async def run_bot():
    """Main bot entry point."""
    # Initialize database
    repo = get_user_repo(settings.database_url)
    await repo.init()

    # Create bot and dispatcher
    bot, dp = await create_bot_and_dispatcher(repo)

    try:
        # Start polling
        print("Bot started. Press Ctrl+C to stop.")
        await dp.start_polling(bot)
    finally:
        await repo.close()
        await bot.session.close()
