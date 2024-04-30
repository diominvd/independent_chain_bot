from aiogram.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    admin_panel = State()

    mailing_ru = State()
    mailing_en = State()

    mail_username = State()
    mail_message = State()

    statistics = State()