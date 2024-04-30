from aiogram.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    waiting_wallet = State()
    events_menu = State()


class EventsStates(StatesGroup):
    raffle_nft = State()