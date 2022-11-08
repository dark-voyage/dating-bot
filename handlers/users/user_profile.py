from aiogram.types import CallbackQuery

from handlers.users.back_handler import delete_message
from keyboards.inline.menu_profile_inline import get_profile_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.get_data_func import get_data


@dp.callback_query_handler(text="my_profile")
async def my_profile_menu(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    await delete_message(call.message)
    # user_db = await db_commands.select_user(telegram_id=telegram_id)
    markup = await get_profile_keyboard()
    await call.message.answer_photo(photo=user_data['photo_id'])
    await call.message.answer(text=f"<b>Sizni anketangiz:</b>\n\n"
                                   f"{str(user_data['name'])}, {str(user_data['age'])},"
                                   f"{str(user_data['region'])}({str(user_data['city'])}) "
                                   f"\n\n"
                                   f"Millat: {str(user_data['nation'])}\n"
                                   f"Ma'lumot: {str(user_data['education'])}\n"
                                   f"Ish: {str(user_data['job'])}\n"
                                   f"Turmush holati: {str(user_data['lifestyle'])}\n"
                                   f"<b>Qo'shimcha ma'lumot</b> - {str(user_data['commentary'])}\n\n",
                              reply_markup=markup)

@dp.callback_query_handler(text="disable")
async def disable_profile(call: CallbackQuery):
    await db_commands.delete_user(telegram_id=call.from_user.id)
    await delete_message(call.message)
    await call.message.answer("Ваша анкета удалена!\nЯ надеюсь вы кого-нибудь нашли")
