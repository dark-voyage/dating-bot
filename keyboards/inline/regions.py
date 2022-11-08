from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from django_project.telegrambot.usersmanage.models import RegionChoices


async def region_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    Toshkent = InlineKeyboardButton(text="", callback_data="Toshkent")
    Sirdaryo = InlineKeyboardButton(text="Sirdaryo", callback_data="Sirdaryo")
    Jizzax = InlineKeyboardButton(text="Jizzax", callback_data="Jizzax")
    Fargona = InlineKeyboardButton(text="Farg'ona", callback_data="Farg'ona")
    Namangan = InlineKeyboardButton(text="Namangan", callback_data="Namangan")
    Andijon = InlineKeyboardButton(text="Andijon", callback_data="Andijon")
    Surxondaryo = InlineKeyboardButton(text="Surxondaryo", callback_data="Surxondaryo")
    Qashqadaryo = InlineKeyboardButton(text="Qashqadaryo", callback_data="Qashqadaryo")
    Navoiy = InlineKeyboardButton(text="Navoiy", callback_data="Navoiy")
    Buxoro = InlineKeyboardButton(text="Buxoro", callback_data="Buxoro")
    Samarqand = InlineKeyboardButton(text="Samarqand", callback_data="Samarqand")
    Xorazm = InlineKeyboardButton(text="Xorazm", callback_data="Xorazm")
    Qoraqalpogiston = InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="Qoraqalpog'iston")

    markup.row(Toshkent, Sirdaryo, Jizzax)
    markup.row(Fargona, Namangan, Andijon)
    markup.row(Navoiy, Buxoro, Samarqand)
    markup.row(Surxondaryo, Qashqadaryo)
    markup.row(Xorazm, Qoraqalpogiston)
    return markup


async def region_reply_keyboard() -> InlineKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row("Toshkent", "Sirdaryo", "Jizzax")
    markup.row("Farg'ona", "Namangan", "Andijon")
    markup.row("Navoiy", "Buxoro", "Samarqand")
    markup.row("Surxondaryo", "Qashqadaryo")
    markup.row("Xorazm", "Qoraqalpog'iston")
    return markup
