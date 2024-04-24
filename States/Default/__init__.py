from aiogram.filters.state import StatesGroup, State


class DefaultStates(StatesGroup):
    check_subscribe = State()
    get_wallet = State()
    information = State()