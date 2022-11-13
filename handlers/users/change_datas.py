import asyncio
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from aiogram.utils.markdown import quote_html
from loguru import logger

from handlers.users.back_handler import delete_message
from keyboards.inline.change_data_profile_inline import change_info_keyboard, gender_keyboard
from keyboards.inline.regions import region_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp
from states.new_data_state import NewData
from utils.db_api import db_commands
from utils.misc.profanityFilter import censored_message


@dp.callback_query_handler(text='change_profile')
async def start_change_data(call: CallbackQuery):
    markup = await change_info_keyboard()
    await delete_message(call.message)
    await call.message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)


@dp.callback_query_handler(text='name')
async def change_name(call: CallbackQuery):
    await call.message.edit_text(f'Введите новое имя')
    await NewData.name.set()


@dp.message_handler(state=NewData.name)
async def change_name(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(name=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f'Sizni yangi ismingiz: <b>{censored}</b>')
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f"Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring", reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='age')
async def change_age(call: CallbackQuery):
    await call.message.edit_text(f'Yangi yoshni yozing')
    await NewData.age.set()


@dp.message_handler(state=NewData.age)
async def change_age(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        if int(message.text) and 0 < int(message.text) < 110:
            await db_commands.update_user_data(age=message.text, telegram_id=message.from_user.id)
            await message.answer(f'Sizni yangi yoshingiz: <b>{message.text}</b>')
            await asyncio.sleep(3)
            await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
            await state.reset_state()
        else:
            await message.answer(f"Noto'g'ri ma'lumotlar. Qayta urinib ko'ring", reply_markup=markup)
            await state.reset_state()

    except Exception as err:
        logger.error(err)
        await message.answer(f"Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring", reply_markup=markup)
        await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='city')
async def change_city(call: CallbackQuery):
    await call.message.edit_text(f'Введите новый город')
    await NewData.city.set()


@dp.message_handler(state=NewData.city)
async def change_city(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(varname=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f'Sizni yangi shahringiz: <b>{censored}</b>')
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f"Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring", reply_markup=markup)
        await state.reset_state()


@dp.callback_query_handler(text='region')
async def change_region(call: CallbackQuery):
    markup = await region_keyboard()
    await call.message.edit_text(f'Viloyatingizni tanlang: ', reply_markup=markup)
    await NewData.region.set()


@dp.callback_query_handler(state=NewData.region)
async def change_region(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    print(call, call.data)
    try:
        await db_commands.update_user_data(region=call.data, telegram_id=call.from_user.id)
        await call.message.edit_text(f'Sizni yangi jinsingiz: <b>{call.data}</b>')
        await asyncio.sleep(1)
        await call.message.edit_text(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await call.message.edit_text(f"Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring", reply_markup=markup)
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text="yes_all_good", state=NewData.city)
async def get_hobbies(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Ma'lumotlar o'zgartirildi.\nNimani o'zgartirmoqchi bo'lganizni tanlang: ",
                                 reply_markup=await change_info_keyboard())
    await state.reset_state()


@dp.callback_query_handler(text='gender')
async def change_sex(call: CallbackQuery):
    markup = await gender_keyboard()
    await call.message.edit_text(f'Yangi jinsni tanlang: ', reply_markup=markup)
    await NewData.sex.set()


@dp.callback_query_handler(state=NewData.sex)
async def change_sex(call: CallbackQuery, state: FSMContext):
    markup = await change_info_keyboard()
    print(call, call.data)
    if call.data == 'male':
        try:
            await db_commands.update_user_data(sex='Erkak', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Sizni yangi jinsingiz: <b>Erkak</b>')
            await asyncio.sleep(3)
            await call.message.edit_text(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f"Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring", reply_markup=markup)
            await state.reset_state()
    if call.data == 'female':
        try:
            await db_commands.update_user_data(sex='Ayol', telegram_id=call.from_user.id)
            await call.message.edit_text(f'Sizni yangi jinsingiz: <b>Ayol</b>')
            await asyncio.sleep(3)
            await call.message.edit_text(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
            await state.reset_state()
        except Exception as err:
            logger.error(err)
            await call.message.edit_text(f"Noaniq xatolik yuz berdi! Iltimos qayta urinib ko'ring", reply_markup=markup)
            await state.reset_state()

    await state.reset_state()


@dp.callback_query_handler(text='job')
async def change_job(call: CallbackQuery):
    await call.message.edit_text(f"Kasbingiz nima?")
    await NewData.job.set()


@dp.message_handler(state=NewData.job)
async def change_job(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(job=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f"Ma'lumotlar o'zgaritirildi!")
        await asyncio.sleep(2)
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Noaniq xatolik yuz berdi', reply_markup=markup)
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text='lifestyle')
async def change_style(call: CallbackQuery):
    await call.message.edit_text(f'Turmush holatingiz qanday?')
    await NewData.lifestyle.set()


@dp.message_handler(state=NewData.lifestyle)
async def change_style(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(lifestyle=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f"Ma'lumotlar o'zgaritirildi!")
        await asyncio.sleep(2)
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Noaniq xatolik yuz berdi', reply_markup=markup)
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text='education')
async def change_education(call: CallbackQuery):
    await call.message.edit_text(f"Ma'lumotingiz qanday?")
    await NewData.education.set()


@dp.message_handler(state=NewData.education)
async def change_education(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(education=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f"Ma'lumotlar o'zgaritirildi!")
        await asyncio.sleep(2)
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Noaniq xatolik yuz berdi', reply_markup=markup)
        await state.reset_state()
    await state.reset_state()


@dp.callback_query_handler(text='nation')
async def change_nation(call: CallbackQuery):
    await call.message.edit_text(f"Qaysi millatdansiz?")
    await NewData.nation.set()


@dp.message_handler(state=NewData.nation)
async def change_nation(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(nation=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f"Ma'lumotlar o'zgaritirildi!")
        await asyncio.sleep(2)
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Noaniq xatolik yuz berdi', reply_markup=markup)
        await state.reset_state()
    await state.reset_state()

@dp.callback_query_handler(text='photo')
async def new_photo(call: CallbackQuery):
    await call.message.edit_text(f'Yangi fotoni yuboring')
    await NewData.photo.set()
    await asyncio.sleep(3)
    await delete_message(call.message)


@dp.message_handler(content_types=ContentType.PHOTO, state=NewData.photo)
async def update_photo_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    file_id = message.photo[-1].file_id
    try:
        await db_commands.update_user_data(photo_id=file_id, telegram_id=message.from_user.id)
        await message.answer(f'Foto qabul qilindi!')
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                             f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()


@dp.callback_query_handler(text='about_me')
async def new_comment(call: CallbackQuery):
    await call.message.edit_text(f'Anketangizni yangi tavsifini yuboring(maksimal 255 ta simvol) : ')
    await NewData.commentary.set()


@dp.message_handler(state=NewData.commentary)
async def update_comment_complete(message: types.Message, state: FSMContext):
    markup = await change_info_keyboard()
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(commentary=quote_html(censored), telegram_id=message.from_user.id)
        await message.answer(f'Kommentariy qabul qilindi!')
        await asyncio.sleep(3)
        await delete_message(message)
        await message.answer(f"Nimani o'zgartirmoqchi bo'lganizni tanlang: ", reply_markup=markup)
        await state.reset_state()
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз изменить описание. '
                             f'Возможно, Ваше сообщение слишком большое\n'
                             f'Если ошибка осталась, напишите системному администратору.')
        await state.reset_state()
