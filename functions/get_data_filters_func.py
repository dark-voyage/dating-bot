from utils.db_api import db_commands


async def get_data_filters(telegram_id: int) -> tuple[int, int, str, str]:
    user = await db_commands.select_user(telegram_id=telegram_id)
    user_need_age_min = user.get("need_partner_age_min")
    user_need_age_max = user.get("need_partner_age_max")
    user_need_gender = user.get("need_partner_sex")
    user_need_region = user.get("region")

    return user_need_age_min, user_need_age_max, user_need_gender, user_need_region
