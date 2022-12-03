from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

action_keyboard = CallbackData("questionnaire", "action", "target_id")
action_keyboard_monitoring = CallbackData("questionnaire_monitoring", "action", "target_id")
action_reciprocity_keyboard = CallbackData("questionnaire", "action", "user_for_like")


async def questionnaires_keyboard(target_id, monitoring=False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    if not monitoring:
        like = InlineKeyboardButton(text='👍', callback_data=action_keyboard.new(action="like",
                                                                                 target_id=target_id))
        dislike = InlineKeyboardButton(text='👎', callback_data=action_keyboard.new(action="dislike",
                                                                                    target_id=1))
        go_back = InlineKeyboardButton(text=f"⏪️ To'xtatmoq",
                                       callback_data=action_keyboard.new(action="stopped",
                                                                         target_id=1))
        markup.row(like, dislike)
        markup.add(go_back)
        return markup
    else:
        ban = InlineKeyboardButton(text='🚫 Забанить',
                                   callback_data=action_keyboard_monitoring.new(action="ban",
                                                                                target_id=target_id))

        next_btn = InlineKeyboardButton(text='Следующий', callback_data=action_keyboard_monitoring.new(action="next",
                                                                                                       target_id=1))
        markup.row(ban)
        markup.row(next_btn)
        return markup


async def reciprocity_keyboard(user_for_like) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    like = InlineKeyboardButton(text='👍', callback_data=action_reciprocity_keyboard.new(action="like_reciprocity",
                                                                                         user_for_like=user_for_like))
    dislike = InlineKeyboardButton(text='👎',
                                   callback_data=action_reciprocity_keyboard.new(action="dislike_reciprocity",
                                                                                 user_for_like=1))
    markup.row(like, dislike)

    return markup


async def back_viewing_ques_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(text='Anketalarni kuzatishga qaytish', callback_data="go_back_to_viewing_ques")
    markup.row(back)

    return markup
