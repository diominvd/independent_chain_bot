from aiogram.fsm.state import StatesGroup, State


class WalletStates(StatesGroup):
    address = State()


class CodesStates(StatesGroup):
    code = State()