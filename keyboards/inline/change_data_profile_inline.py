from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def change_info_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    name = InlineKeyboardButton(text="Ism", callback_data="name")
    gender = InlineKeyboardButton(text="Jins", callback_data="gender")
    age = InlineKeyboardButton(text="Yosh", callback_data="age")
    region = InlineKeyboardButton(text="Viloyat", callback_data="region")
    city = InlineKeyboardButton(text="Shahar", callback_data="city")
    nation = InlineKeyboardButton(text="Millat", callback_data="nation")
    education = InlineKeyboardButton(text="Ma'lumot", callback_data="education")
    lifestyle = InlineKeyboardButton(text="Turmush holati", callback_data="lifestyle")
    employment = InlineKeyboardButton(text="Kasb", callback_data="job")
    photo = InlineKeyboardButton(text="Foto", callback_data="photo")
    about_me = InlineKeyboardButton(text="O'z haqizda", callback_data="about_me")
    back_to_menu = InlineKeyboardButton(text="⏪️ Menuga qaytish", callback_data="back_with_delete")
    markup.row(name, gender, age, )
    markup.row(region, city, nation, )
    markup.row(education, lifestyle)
    markup.row(employment, photo, about_me)
    markup.add(back_to_menu)
    return markup


async def gender_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    male = InlineKeyboardButton(text='Erkak', callback_data='male')
    female = InlineKeyboardButton(text='Ayol', callback_data='female')
    markup.row(male, female)
    return markup
