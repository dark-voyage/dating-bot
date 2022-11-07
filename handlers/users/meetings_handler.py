from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from loader import dp
from utils.db_api import db_commands
from functions.get_data_func import get_data


