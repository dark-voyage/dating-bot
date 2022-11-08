from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State


class NewData(StatesGroup):
    sex = State()
    commentary = State()
    name = State()
    need_partner_sex = State()
    region = State()
    education = State()
    age = State()
    city = State()
    nation = State()
    education = State()
    town = State()
    car = State()
    own_home = State()
    hobbies = State()
    photo = State()
