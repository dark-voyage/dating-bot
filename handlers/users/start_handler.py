import random

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.config import load_config
from filters import IsPrivate
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp
from utils.db_api import db_commands


@dp.message_handler(IsPrivate(), CommandStart())
async def register_user(message: types.Message):
    try:
        if message.from_user.username is not None:
            await db_commands.add_user(name=message.from_user.full_name,
                                       telegram_id=message.from_user.id,
                                       username=message.from_user.username)

        else:
            await db_commands.add_user(name=message.from_user.full_name,
                                       telegram_id=message.from_user.id,
                                       username="None")


    except:
        pass
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    user_db = await db_commands.select_user(telegram_id=message.from_user.id)
    markup = await start_keyboard(status=user_db["status"])

    heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
    await message.answer(text=f"Приветствую вас, {message.from_user.full_name}!!\n\n"
                              f"{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
                              f"🪧 Новости о проекте вы можете прочитать в нашем канале - "
                              f"https://t.me/QueDateGroup \n\n"
                              f"<b>🤝 Сотрудничество: </b>\n"
                              f"Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
                              f"@{support['username']}\n\n",
                         reply_markup=markup)


@dp.callback_query_handler(text="start_menu")
async def start_menu(call: CallbackQuery):
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    support = await db_commands.select_user(telegram_id=load_config().tg_bot.support_ids[0])
    markup = await start_keyboard(user_db["status"])
    heart = random.choice(['💙', '💚', '💛', '🧡', '💜', '🖤', '❤', '🤍', '💖', '💝'])
    await call.message.edit_text(text=f"Приветствую вас, {call.from_user.full_name}!!\n\n"
                                      f"{heart} <b> QueDateBot </b> - платформа для поиска новых знакомств.\n\n"
                                      f"🪧 Новости о проекте вы можете прочитать в нашем канале - "
                                      f"https://t.me/QueDateGroup \n\n"
                                      f"🤝 <b> Сотрудничество: </b>\n"
                                      f"Если у вас есть предложение о сотрудничестве, пишите агенту поддержки - "
                                      f"@{support['username']}\n\n",
                                 reply_markup=markup)
