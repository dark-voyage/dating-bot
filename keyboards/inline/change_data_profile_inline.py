from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def change_info_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    name = InlineKeyboardButton(text="Имя", callback_data="name")
    gender = InlineKeyboardButton(text="Пол", callback_data="gender")
    age = InlineKeyboardButton(text="Возраст", callback_data="age")
    region = InlineKeyboardButton(text="Viloyat", callback_data="region")
    city = InlineKeyboardButton(text="Город", callback_data="city")
    nation = InlineKeyboardButton(text="Millat", callback_data="nation")
    education = InlineKeyboardButton(text="Ma'lumot", callback_data="education")
    employment = InlineKeyboardButton(text="Занятость", callback_data="job")
    photo = InlineKeyboardButton(text="Фото", callback_data="photo")
    about_me = InlineKeyboardButton(text="О себе", callback_data="about_me")
    back_to_menu = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="back_with_delete")
    markup.row(name, gender, age)
    markup.row(region, city, nation, education)
    markup.row(employment, photo, about_me)
    markup.add(back_to_menu)
    return markup


async def gender_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    male = InlineKeyboardButton(text='Парень', callback_data='male')
    female = InlineKeyboardButton(text='Девушка', callback_data='female')
    markup.row(male, female)
    return markup
