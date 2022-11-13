from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound
from loguru import logger

from data.config import load_config


async def on_startup_notify(dp: Dispatcher):
    logger.info("Administratsiya ogohlantiruvi...")
    for admin in load_config().tg_bot.admin_ids:
        try:
            await dp.bot.send_message(
                admin, "Bot ishga tushirildi", disable_notification=True
            )
        except ChatNotFound:
            logger.debug("Admin bilan chat topilmadi")
