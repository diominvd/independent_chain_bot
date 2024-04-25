from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import database as db


def update_last_activity(func):
    async def wrapper(obj: Message | CallbackQuery, state: FSMContext):
        db.update_last_activity(user_id=obj.from_user.id)
        return await func(obj, state)
    return wrapper