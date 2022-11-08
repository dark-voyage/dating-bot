from aiogram.dispatcher.filters.state import State, StatesGroup


class RegData(StatesGroup):
    sex = State()
    commentary = State()
    name = State()
    region = State()
    age = State()
    nation = State()
    education = State()
    town = State()
    job = State()
    lifestyle = State()
    photo = State()
