from aiogram.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    waiting_wallet = State()


class EventsStates(StatesGroup):
    events_menu = State()
    raffle_nft = State()