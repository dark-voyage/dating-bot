from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main_menu_inline import start_keyboard
from keyboards.inline.registration_inline import registration_keyboard
from keyboards.inline.support_inline import support_keyboard, support_callback, check_support_available, \
    get_support_manager, \
    cancel_support, cancel_support_callback
from loader import dp, bot
from utils.db_api import db_commands
from functions.get_data_func import get_data


@dp.callback_query_handler(text="support")
async def ask_support_call(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    user_data = await get_data(telegram_id)
    user_status = user_data["status"]
    if user_status:
        text = "Texnik yordam bilan suhbat uchun pastadgi knopkani bosing"
        keyboard = await support_keyboard(messages="many")
        if not keyboard:
            await call.message.edit_text("Uzr, hozirda operatorimiz bilan suhbat qura olmaysiz. Keyinroq harakat qiling!")
            return
        await call.message.edit_text(text, reply_markup=keyboard)
    else:
        await call.message.edit_text("Siz registratsiya qilishingiz kerak, pastdagi knopkani bosing",
                                     reply_markup=await registration_keyboard())


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="yes"))
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text("Operator javobini kuting!")

    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id

    if not support_id:
        await call.message.edit_text("Hozirchalik bo'sh operatorlar yo'q, keyinroq harakat qilib ko'ring")
        await state.reset_state()
        return

    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(messages="many", user_id=call.from_user.id)

    await bot.send_message(support_id,
                           f"Siz bilan bog'lnamoqchi {call.from_user.full_name}",
                           reply_markup=keyboard
                           )


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="no"))
async def answer_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("Foydalanuvchi yo'q dedi.")
        return

    await state.set_state("in_support")
    await user_state.set_state("in_support")

    await state.update_data(second_id=second_id)

    keyboard = cancel_support(second_id)
    keyboard_second_user = cancel_support(call.from_user.id)

    await call.message.edit_text("Siz foydalanuvchi bilan aloqadasiz!\n"
                                 "To'xtatish uchun knopkani bosing.",
                                 reply_markup=keyboard
                                 )

    await bot.send_message(second_id,
                           "Tex yordam siz bilan. \n"
                           "To'xtatish uchun knopkani bosing.",
                           reply_markup=keyboard_second_user
                           )


@dp.message_handler(state="wait_in_support", content_types=types.ContentTypes.ANY)
async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    keyboard = cancel_support(second_id)
    await message.answer("Operatordan javobni kuting", reply_markup=keyboard)


@dp.callback_query_handler(cancel_support_callback.filter(), state=["in_support", "wait_in_support", None])
async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_db = await db_commands.select_user(telegram_id=call.from_user.id)
    markup = await start_keyboard(status=user_db["status"])
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        data = await state.get_data()
        second_id = data.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await bot.send_message(user_id, "Foydalanuvchi to'xtatdi seansni")

    await call.message.edit_text("Siz seansni yakunladingiz", reply_markup=markup)
    await state.reset_state()
