from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.config import settings
from bot.services.user_service import UserService
from bot.i18n import i18n

router = Router()


class BroadcastState(StatesGroup):
    waiting_for_message = State()


async def setup_broadcast_handler(user_service: UserService):
    @router.message(Command("broadcast"))
    async def broadcast_command(message: types.Message, state: FSMContext):
        if message.from_user.id != settings.admin_id:
            # Get admin's language
            admin_user = await user_service.get_user(message.from_user.id)
            admin_lang = admin_user.language if admin_user else "uz"
            await message.answer(i18n.get("admin_only", admin_lang))
            return

        # Get admin's language
        admin_user = await user_service.get_user(message.from_user.id)
        admin_lang = admin_user.language if admin_user else "uz"

        await message.answer(i18n.get("broadcast_prompt", admin_lang))
        await state.set_state(BroadcastState.waiting_for_message)

    @router.message(BroadcastState.waiting_for_message)
    async def handle_broadcast_message(message: types.Message, state: FSMContext):
        users = await user_service.get_all_users()
        
        # Get admin's language
        admin_user = await user_service.get_user(message.from_user.id)
        admin_lang = admin_user.language if admin_user else "uz"

        # Extract the message to forward/send
        if message.forward_from:
            # If it's a forwarded message, forward it to all users
            sent_count = 0
            for user in users:
                try:
                    await message.forward(user.tg_id)
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending to {user.tg_id}: {e}")
        else:
            # If it's a regular message, copy it to all users
            sent_count = 0
            for user in users:
                try:
                    # Copy message with all content (text, media, etc.)
                    await message.copy_to(user.tg_id)
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending to {user.tg_id}: {e}")

        result_text = i18n.get("broadcast_sent", admin_lang, count=sent_count)
        await message.answer(result_text)
        await state.clear()

    return router
