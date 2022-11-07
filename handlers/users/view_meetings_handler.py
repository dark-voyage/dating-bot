import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


from handlers.users.back_handler import delete_message
from keyboards.inline.main_menu_inline import start_keyboard
from loader import dp
from utils.db_api import db_commands



@dp.callback_query_handler(state='finding_meetings', text="stopped")
async def like_questionnaire(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    markup = await start_keyboard(status=user_db['status'])
    await call.message.delete()
    await call.message.answer(f"Рад был помочь, {call.from_user.full_name}!\n"
                              f"Надеюсь, ты нашел кого-то благодаря мне", reply_markup=markup)
    await state.reset_state()
