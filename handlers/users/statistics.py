from aiogram.types import CallbackQuery
from keyboards.inline.registration_inline import registration_keyboard
from keyboards.inline.sponsor_inline import sponsors_keyboard
from loader import dp
from utils.db_api import db_commands
from functions.get_data_func import get_data


@dp.callback_query_handler(text="statistics")
async def get_inst(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_city = user_data["city"]
    user_status = user_data["status"]
    users_gender_m = await db_commands.count_all_users_kwarg(sex="Erkak")
    users_gender_f = await db_commands.count_all_users_kwarg(sex="Ayol")
    users_city = await db_commands.count_all_users_kwarg(city=user_city)
    users_status = await db_commands.count_all_users_kwarg(status=True)
    if user_status:
        count_users = await db_commands.count_users()
        await call.message.edit_text(f"<b>📊 Статистика: </b>\n\n"
                                     f"└Сейчас в нашем боте <b>{count_users} пользователей</b>\n"
                                     f"└Из них:\n"
                                     f"        ├<b>{users_gender_m} пользователей мужского пола</b>\n"
                                     f"        ├<b>{users_gender_f} пользователей женского пола</b>\n"
                                     f"        ├<b>{users_city} пользователей из города {user_city}</b>\n"
                                     f"        ├<b>{count_users - users_city} пользователей из других городов</b>\n"
                                         f"        ├<b>{users_status} пользователей, создавшие анкету</b>\n"
                                     f"└Дата создания бота - <b>10.08.2021</b>", reply_markup=await sponsors_keyboard()
                                     )
    else:
        await call.message.edit_text("Вам необходимо зарегистрироваться, нажмите на кнопку ниже",
                                     reply_markup=await registration_keyboard())
