from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def filters_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    user_age_period = InlineKeyboardButton(text="🔞 Возр.диапазон", callback_data='user_age_period')
    back = InlineKeyboardButton(text="⏪️ Назад", callback_data="back_with_delete")
    markup.row(user_age_period)
    markup.add(back)
    return markup
