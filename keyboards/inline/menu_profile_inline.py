from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_profile_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    # if not verification:
    #     verification_btn = InlineKeyboardButton(text="✅ Верификация", callback_data="verification")
    #     markup.row(verification_btn)
    edit_profile = InlineKeyboardButton(text="Изменить анкету", callback_data="change_profile")
    turn_off = InlineKeyboardButton(text="❌ Удалить анкету", callback_data="disable")
    back = InlineKeyboardButton(text="⏪ Назад", callback_data="back_with_delete")
    markup.row(edit_profile)
    markup.add(turn_off)
    markup.add(back)
    return markup
