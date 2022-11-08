from utils.db_api import db_commands


async def get_data(telegram_id: int) -> dict:
    user = await db_commands.select_user(telegram_id=telegram_id)
    d = dict()

    d['name'] = user.get("name", "Noaniq")
    d['age'] = user.get("age", 39)
    d['sex'] = user.get("sex", "male")
    d['region'] = user.get("region", "Noaniq")
    d['city'] = user.get("city", "Noaniq")
    d['lifestyle'] = user.get("lifestyle", "Noaniq")
    d['commentary'] = user.get("commentary", "Noaniq")
    d['nation'] = user.get("nation", "Noaniq")
    d['education'] = user.get("education", "Noaniq")
    d['job'] = user.get("job", "Noaniq")
    d['photo_id'] = user.get("photo_id", "https://www.meme-arsenal.com/memes/5eae5104f379baa355e031fa1ded886c.jpg")
    d['status'] = user.get("status", None)
    d['need_partner_sex'] = user.get("need_partner_sex", "female")

    return d
