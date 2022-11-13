from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def registration_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    registration = InlineKeyboardButton(text="➕ Registratsiya", callback_data="registration")
    markup.add(registration)
    return markup


async def second_registration_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    questionnaire = InlineKeyboardButton(text="Anketani to'ldirish", callback_data="survey")
    back_to_menu = InlineKeyboardButton(text="⏪️ Menuga qaytish", callback_data="start_menu")
    markup.add(questionnaire, back_to_menu)
    return markup


async def confirm_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    yes_all_good = InlineKeyboardButton(text=f"Barchasi yaxshi!", callback_data="yes_all_good")
    markup.add(yes_all_good)
    return markup
