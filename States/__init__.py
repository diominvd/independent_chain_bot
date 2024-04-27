from aiogram.filters.state import StatesGroup, State


class DefaultStates(StatesGroup):
    check_subscribe = State()
    profile = State()
    wallet = State()
    information = State()
    support = State()