from keyboards.inline.questionnaires_inline import questionnaires_keyboard, back_viewing_ques_keyboard, \
    reciprocity_keyboard
from loader import bot


async def send_questionnaire(chat_id, user_data, user_db, markup=None, add_text=None,
                             monitoring=False):
    user_telegram_id = user_db.get("telegram_id")
    if add_text is None:
        await bot.send_photo(chat_id=chat_id,
                             caption=f"{str(user_data['name'])}, {str(user_data['age'])}, {str(user_data['region'])}({str(user_data['city'])}) "
                                     f"\n\n"
                                     f"Millat: {str(user_data['nation'])}\n"
                                     f"Ma'lumot: {str(user_data['education'])}\n"
                                     f"Ish: {str(user_data['job'])}\n"
                                     f"Turmush holati: {str(user_data['lifestyle'])}\n"
                                     f"<b>Qo'shimcha ma'lumot</b> - {str(user_data['commentary'])}\n\n",
                             photo=user_data['photo_id'],
                             reply_markup=await questionnaires_keyboard(target_id=user_telegram_id,
                                                                        monitoring=monitoring))
    elif markup is None:
        await bot.send_photo(chat_id=chat_id,
                             caption=f"{add_text} \n{str(user_data['name'])}, {str(user_data['age'])}, {str(user_data['region'])}({str(user_data['city'])}) "
                                                f"\n\n"
                                                f"Millat: {str(user_data['nation'])}\n"
                                                f"Ma'lumot: {str(user_data['education'])}\n"
                                                f"Ish: {str(user_data['job'])}\n"
                                                f"Turmush holati: {str(user_data['lifestyle'])}\n"
                                                f"<b>Qo'shimcha ma'lumot</b> - {str(user_data['commentary'])}\n\n",
                             photo=user_data['photo_id'], reply_markup=await back_viewing_ques_keyboard())

    else:
        await bot.send_photo(chat_id=chat_id,
                             caption=f"{add_text} \n{str(user_data['name'])}, {str(user_data['age'])}, {str(user_data['region'])}({str(user_data['city'])}) "
                                                f"\n\n"
                                                f"Millat: {str(user_data['nation'])}\n"
                                                f"Ma'lumot: {str(user_data['education'])}\n"
                                                f"Ish: {str(user_data['job'])}\n"
                                                f"Turmush holati: {str(user_data['lifestyle'])}\n"
                                                f"<b>Qo'shimcha ma'lumot</b> - {str(user_data['commentary'])}\n\n",
                             photo=user_data['photo_id'],
                             reply_markup=await reciprocity_keyboard(user_for_like=user_telegram_id))
