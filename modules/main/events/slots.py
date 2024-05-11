from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table
from markdown import Markdown
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "slots")
@users_table.update_last_activity
async def slots(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "slots": {
            "ru": (f"{Markdown.bold('Добро пожаловать в слоты')} 🎰\n\n"
                   f"{Markdown.bold('Ставка по умолчанию')}: 10 $tINCH\n\n"
                   f"В случае выпадения трёх одинаковых слотов вы получаете выйгрыш в размере x15 от начальной ставки.\n\n"
                   f"Если на слотах выпадет три бриллианта - ваш выйгрыш составит х20 от начальной ставки 🤑"),
            "en": (f"{Markdown.bold('Welcome to Slots')} 🎰\n\n"
                   f"{Markdown.bold('Default bet')}: 10$tINCH\n\n"
                   f" If three identical slots fall out, you get a win of x15 of the initial bet.\n\n"
                   f" If three brilliants appear on the slots - you winnings will be to x20 of the initial bet 🤑")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(MainModuleStates.slots)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "slots"),
        reply_markup=MainModule.modules["events"].keyboard_slots(callback))
    return None


@MainModule.router.callback_query(F.data == "spin")
@users_table.update_last_activity
async def spin(callback: CallbackQuery, state: FSMContext) -> None:
    if users_table.get_value("balance", "user_id", callback.from_user.id) > 10:
        users_table.update_balance(callback.from_user.id, "-", 10)

        result, reward = MainModule.modules["events"].spin()

        strings: dict[str, dict] = {
            "win_alert": {
                "ru": (f"{result}\n\n"
                       f"Поздравляем! Вы выйграли {reward} $tINCH."),
                "en": (f"{result}\n\n"
                       f"Congratulations! You have won {reward} $tINCH."),
            },
            "lose_alert": {
                "ru": (f"{result}\n\n"
                       "Вы проиграли 10 $tINCH. Попробуйте ещё раз!"),
                "en": (f"{result}\n\n"
                       "You've lost 10 $tINCH. Try again!")
            }
        }

        if reward == 0:
            await callback.answer(
                text=Translator.text(callback, strings, "lose_alert"),
                show_alert=True)
        else:
            users_table.update_balance(callback.from_user.id, "+", reward)
            await callback.answer(
                text=Translator.text(callback, strings, "win_alert"),
                show_alert=True)
        return None

    else:
        strings: dict[str, dict] = {
            "alert": {
                "ru": "Недостаточно $tINCH для игры.",
                "en": "Not enough $tINCH to play."
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "alert"),
            show_alert=True)
        return None