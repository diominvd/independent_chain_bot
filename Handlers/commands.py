from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Keyboards import start_keyboard
import strings
from States import BotStates
from config import dispatcher, database
from strings import translate_answer, translate_button
import utils as u


"""
В каждый handler добавлена проверка подписки на каналы проекта. Если пользователь не подписан - бот не пускает дальше.
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        ...
"""


@dispatcher.message(Command("start"))
async def start_handler(message: Message) -> None:
    # Fetch uer data.
    telegram_id: int = u.fetch_user_id(message)
    username: str = u.fetch_username(message)
    user_language: str = u.fetch_user_language(message)
    registration_date: str = u.fetch_registration_date(message)
    inviter_id: int = u.fetch_inviter_id(message)
    message_text: str = u.fetch_message_text(message)
    # Check subscribe on channels.
    # Check user in database.
    if not database.check_user(telegram_id):
        database.create_user(telegram_id, username, user_language, registration_date, inviter_id)
        database.add_referal(inviter_id)
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        # Answer with correct language.
        answer_text: str = translate_answer(message_text, user_language)
        await message.answer(answer_text)


@dispatcher.message(Command("info"))
async def info_handler(message: Message) -> None:
    user_language: str = u.fetch_user_language(message)
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        answer_text: str = translate_answer(message.text, user_language)
        await message.answer(answer_text)


@dispatcher.message(Command("profile"))
async def profile_handler(message: Message) -> None:
    user_language: str = u.fetch_user_language(message)
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        user_id: int = u.fetch_user_id(message)
        profile_data = database.load_profile(user_id)
        print(profile_data)
        answer_text: str = translate_answer(message.text, user_language, profile_data)
        await message.answer(answer_text)


@dispatcher.message(Command("wallet"))
async def wallet_handler(message: Message, state: FSMContext) -> None:
    """
    Функция ловит команду /wallet и перекидывает в состояние ниже, для получения адреса кошелька.
    """
    user_language: str = u.fetch_user_language(message)
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        await message.answer(text=strings.translate_answer("wallet_request", user_language))
        await state.set_state(BotStates.first_start)


@dispatcher.message(StateFilter(BotStates.first_start))
async def wallet_address_handler(message: Message, state: FSMContext) -> None:
    """
    Функция ожидает адрес кошелька от пользователя. После получения проверяет на корректность. Если адрес корректен -
    записывает адрес в БД. Если адрес некорректен - просит отправить еще раз.
    """
    user_language: str = u.fetch_user_language(message)
    user_id: int = u.fetch_user_id(message)
    wallet_address: str = message.text
    if len(wallet_address) < 40:
        await message.answer(text=strings.translate_answer("wallet_accept_error", user_language))
    elif len(wallet_address) > 40:
        database.add_user_wallet(user_id, wallet_address)
        await message.answer(text=strings.translate_answer("wallet_accept", user_language))
        await state.clear()


@dispatcher.message(Command("links"))
async def links_handler(message: Message) -> None:
    user_language = u.fetch_user_language(message)
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        answer_text: str = translate_answer(message.text, user_language)
        await message.answer(answer_text)


@dispatcher.message(Command("coin"))
async def coin_handler(message: Message) -> None:
    user_language = u.fetch_user_language(message)
    if not await u.subscribe_check(message):
        answer_text: str = strings.translate_answer("subscribe", user_language)
        keyboard = start_keyboard(user_language)
        await message.answer(answer_text, reply_markup=keyboard)
    else:
        answer_text: str = translate_answer(message.text, user_language)
        await message.answer(answer_text)
