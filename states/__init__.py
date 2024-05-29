from aiogram.fsm.state import StatesGroup, State


class WalletStates(StatesGroup):
    address = State()


class CodesStates(StatesGroup):
    code = State()


class AdminStates(StatesGroup):
    mailing = State()
    constants = State()
    generate_codes = State()
    get_codes = State()