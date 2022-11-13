from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard(status) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    if not status:
        registration = InlineKeyboardButton(text="➕ REGISTRATSIYA", callback_data="registration")
        information = InlineKeyboardButton(text="🌐 HAMKORLIK", callback_data="info")
        support = InlineKeyboardButton(text="🆘 YORDAM", callback_data="support")
        markup.row(registration)
        markup.row(support, information)
        return markup
    else:
        my_profile = InlineKeyboardButton(text="👤 Mening anketam", callback_data="my_profile")
        filters = InlineKeyboardButton(text="⚙️ Filtrlar", callback_data="filters")
        view_ques = InlineKeyboardButton(text="💌 Yor izlash", callback_data="find_ancets")
        information = InlineKeyboardButton(text="🌐 Qo'llanma", callback_data="info")
        statistics = InlineKeyboardButton(text="📈 Statistika", callback_data="statistics")
        support = InlineKeyboardButton(text="🆘 Yordam", callback_data="support")
        markup.row(my_profile, filters)
        markup.row(view_ques)
        markup.row(information, statistics)
        markup.add(support)
        return markup
