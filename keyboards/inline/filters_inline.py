from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def filters_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    user_age_period = InlineKeyboardButton(text="🔞 Yosh diapazomi", callback_data='user_age_period')
    back = InlineKeyboardButton(text="⏪️ Ortga", callback_data="back_with_delete")
    markup.row(user_age_period)
    markup.add(back)
    return markup
