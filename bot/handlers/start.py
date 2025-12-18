from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.user_service import UserService
from bot.i18n import i18n

router = Router()


async def setup_start_handler(user_service: UserService):
    @router.message(Command("start"))
    async def start_handler(message: types.Message):
        user = await user_service.register_user(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        
        # Get user's language preference
        user_lang = user.language
        text = i18n.get("start_message", user_lang, first_name=message.from_user.first_name)
        
        # Show language selection inline keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=i18n.get("uz", user_lang), callback_data="lang_uz"),
                InlineKeyboardButton(text=i18n.get("ru", user_lang), callback_data="lang_ru"),
                InlineKeyboardButton(text=i18n.get("en", user_lang), callback_data="lang_en"),
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("lang_"))
    async def language_handler(query: types.CallbackQuery):
        lang_code = query.data.split("_")[1]
        
        # Update user language
        await user_service.update_user_language(query.from_user.id, lang_code)
        
        # Get message in new language
        text = i18n.get("language_selected", lang_code)
        await query.answer(text, show_alert=True)
        await query.message.delete()
        
        # Re-send start message in new language
        user = await user_service.get_user(query.from_user.id)
        start_text = i18n.get("start_message", lang_code, first_name=query.from_user.first_name)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=i18n.get("uz", lang_code), callback_data="lang_uz"),
                InlineKeyboardButton(text=i18n.get("ru", lang_code), callback_data="lang_ru"),
                InlineKeyboardButton(text=i18n.get("en", lang_code), callback_data="lang_en"),
            ]
        ])
        
        await query.message.answer(start_text, reply_markup=keyboard)

    return router
