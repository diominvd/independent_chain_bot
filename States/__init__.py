from aiogram.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    first_start = State()
