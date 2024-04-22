from aiogram.filters.state import StatesGroup, State


class DefaultStates(StatesGroup):
    check_subscribe_state = State()
    wallet_state = State()