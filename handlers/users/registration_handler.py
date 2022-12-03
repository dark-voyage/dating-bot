import asyncio
import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import quote_html
from loguru import logger

from django_project.telegrambot.usersmanage.models import RegionChoices
from functions.auxiliary_tools import choice_gender
from keyboards.default.get_location_default import location_keyboard
from keyboards.inline.change_data_profile_inline import gender_keyboard
from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.regions import region_keyboard, region_reply_keyboard
from keyboards.inline.registration_inline import second_registration_keyboard

from loader import dp
from states.reg_state import RegData

from utils.db_api import db_commands
from functions.get_data_func import get_data
from utils.misc.profanityFilter import censored_message


@dp.callback_query_handler(text='registration')
async def registration(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_status = user_data['status']
    if not user_status:
        markup = await second_registration_keyboard()
        text = f"Registratsiya qilish uchun so'rovdan o'ting"
        await call.message.edit_text(text, reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="⬆️ Anketani o'zgartirish", callback_data="change_profile"))
        await call.message.edit_text(
            "Вы уже зарегистрированы, если вам нужно изменить анкету, то нажмите на кнопку ниже",
            reply_markup=markup)


@dp.callback_query_handler(text_contains="survey")
async def survey(call: CallbackQuery):
    markup = await gender_keyboard()

    await call.message.edit_text("Jinsni tanglang", reply_markup=markup)
    await RegData.sex.set()


@dp.callback_query_handler(state=RegData.sex)
async def sex_reg(call: CallbackQuery):
    if call.data == 'male':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex="Erkak")
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex="Ayol")

        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)
    elif call.data == 'female':
        try:
            await db_commands.update_user_data(telegram_id=call.from_user.id, sex='Ayol')
            await db_commands.update_user_data(telegram_id=call.from_user.id, need_partner_sex="Erkak")
        except asyncpg.exceptions.UniqueViolationError as err:
            logger.error(err)

    await call.message.edit_text(f"Endi o'zingiz haqingizda yozing: \n\n(255 belgilar max.)")
    await RegData.commentary.set()


@dp.message_handler(state=RegData.commentary)
async def commentary_reg(message: types.Message):
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(commentary=quote_html(censored), telegram_id=message.from_user.id)

    except Exception as err:
        logger.error(err)
    await message.answer("Ismingiz nima:")
    await RegData.name.set()


@dp.message_handler(state=RegData.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(telegram_id=message.from_user.id, name=quote_html(censored))

    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Yoshingiz nechada: ")
    await RegData.age.set()


@dp.message_handler(state=RegData.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    censored = censored_message(message.text)
    if censored.isnumeric():
        await db_commands.update_user_data(telegram_id=message.from_user.id, age=quote_html(censored))


        markup = await region_reply_keyboard()
        await message.reply(f'Viloyatingizni tanlang: ', reply_markup=markup)
        await RegData.region.set()
    else:
        await message.answer("Bu son emas")

@dp.message_handler(lambda message: (message.text, message.text) not in RegionChoices.choices, state=RegData.region)
async def get_region(message: types.Message, state: FSMContext):
    return await message.reply("Xato viloyat, itimos klaviaturadan viloyatni tanlang")


@dp.message_handler(state=RegData.region)
async def get_region(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(region=message.text, telegram_id=message.from_user.id)
        await message.reply(f'Sizni viloyatingiz: <b>{message.text}</b>')
        await asyncio.sleep(1)
    except Exception as err:
        logger.error(err)
    await message.reply("Sizni shahringiz:", reply_markup=ReplyKeyboardRemove())
    await RegData.town.set()


@dp.message_handler(state=RegData.town)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    try:
        censored = censored_message(message.text)
        await db_commands.update_user_data(telegram_id=message.from_user.id, city=quote_html(censored))

    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Ishingiz nima:")
    await RegData.job.set()


@dp.message_handler(state=RegData.job)
async def get_job(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, job=quote_html(message.text))
        await state.update_data(job=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Ma'lumotingiz:")
    await RegData.education.set()


@dp.message_handler(state=RegData.education)
async def get_education(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, education=quote_html(message.text))
        await state.update_data(education=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Millatingiz:")
    await RegData.nation.set()


@dp.message_handler(state=RegData.nation)
async def get_nation(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, nation=quote_html(message.text))
        await state.update_data(nation=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer("Hozirdagi turmush holatiz:")
    await RegData.lifestyle.set()


@dp.message_handler(state=RegData.lifestyle)
async def get_lifestyle(message: types.Message, state: FSMContext):
    try:
        await db_commands.update_user_data(telegram_id=message.from_user.id, lifestyle=quote_html(message.text))
        await state.update_data(lifestyle=message.text)
    except asyncpg.exceptions.UniqueViolationError as err:
        logger.error(err)
    await message.answer(f"Foto yuboring(O'zingizniki bo'lsa yaxshiroq)")
    await RegData.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=RegData.photo)
async def get_photo(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    file_id = message.photo[-1].file_id
    try:
        await db_commands.update_user_data(telegram_id=telegram_id, photo_id=file_id)

        await message.answer(f'Фото принято!')
    except Exception as err:
        logger.error(err)
        await message.answer(f'Произошла ошибка! Попробуйте еще раз либо отправьте другую фотографию. \n'
                             f'Если ошибка осталась, напишите системному администратору.')

    await state.finish()
    await db_commands.update_user_data(telegram_id=telegram_id, status=True)

    user_data = await get_data(telegram_id)
    user_db = await db_commands.select_user(telegram_id=telegram_id)
    markup = await start_keyboard(status=user_db['status'])
    await message.answer_photo(caption=f"<b>Sizni anketangiz:</b>\n\n"
                                            f"{str(user_data['name'])}, {str(user_data['age'])}, {str(user_data['region'])}({str(user_data['city'])}) "
                                            f"\n\n"
                                            f"Millat: {str(user_data['nation'])}\n"
                                            f"Ma'lumot: {str(user_data['education'])}\n"
                                            f"Ish: {str(user_data['job'])}\n"
                                            f"Turmush holati: {str(user_data['lifestyle'])}\n"
                                            f"<b>Qo'shimcha ma'lumot</b> - {str(user_data['commentary'])}\n\n",
                                    photo=user_data['photo_id'], reply_markup=ReplyKeyboardRemove())
    await message.answer("Menu: ", reply_markup=markup)
