import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import re

from loguru import logger
from keyboards.inline.filters_inline import filters_keyboard

from loader import dp

from utils.db_api import db_commands
from functions.get_data_filters_func import get_data_filters


@dp.callback_query_handler(text="filters")
async def get_filters(call: CallbackQuery):
    user_data = await get_data_filters(call.from_user.id)
    await call.message.edit_text("Yor izlash bo'yicha filtrlar:\n\n"
                                 f"🔞 Yosh diapazoni: {user_data[0]}-{user_data[1]} yosh\n\n",
                                 reply_markup=await filters_keyboard())


@dp.callback_query_handler(text="user_age_period")
async def desired_age(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Minimal yoshni yozing")
    await state.set_state("age_period")


@dp.message_handler(state="age_period")
async def desired_min_age_state(message: types.Message, state: FSMContext):
    try:

        messages = message.text
        int_message = re.findall('[0-9]+', messages)
        int_messages = "".join(int_message)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_partner_age_min=int_messages)
        await message.answer("Ma'lumotlar saqlandi, maksimal yoshni kirgazing")
        await state.reset_state()
        await state.set_state("max_age_period")

    except Exception as err:
        logger.error(err)
        await message.answer("Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring")


@dp.message_handler(state="max_age_period")
async def desired_max_age_state(message: types.Message, state: FSMContext):
    try:

        messages = message.text
        int_message = re.findall('[0-9]+', messages)
        int_messages = "".join(int_message)
        await db_commands.update_user_data(telegram_id=message.from_user.id, need_partner_age_max=int_messages)
        await message.answer("Ma'lumotlar saqlandi, maksimal yoshni kirgazing")
        await state.finish()
        user_data = await get_data_filters(message.from_user.id)
        await message.answer("Filtrlash:\n\n"
                             f"🔞 Yosh diapazoni: {user_data[0]}-{user_data[1]} yosh\n\n",

                             reply_markup=await filters_keyboard())

    except Exception as err:
        logger.error(err)
        await message.answer("Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring")


