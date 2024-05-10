import asyncio
import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.config import users_table, bot, codes_table
from markdown import Markdown
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "events")
@users_table.update_last_activity
async def events(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "events": {
            "ru": (f"В данном разделе находятся актуальные события и активности 🥳\n\n"
                   f"Для просмотра конкретного события выберите соответствующую кнопку.\n\n"
                   f"{Markdown.bold('Текущие события')}:\n"
                   f"• Промокоды - активируйте промокод и получите награду.\n"
                   f"• Слоты - испытай свою удачу и заработай $tINCH."),
            "en": (f"This section contains current events and activities 🥳\n\n"
                   f"To view a specific event, select the appropriate button.\n\n"
                   f"{Markdown.bold('Current Events')}:\n"
                   f"• Promo codes - activate the promo code and receive a reward.\n"
                   f"• Slots - try your luck and earn $tINCH.")
        }
    }

    await callback.answer(show_alert=False)
    await state.update_data(data={"events_message": callback.message.message_id})

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "events"),
        reply_markup=MainModule.modules["events"].keyboard(callback))
    return None


# Promo codes -> ...
@MainModule.router.callback_query(F.data == "codes")
@users_table.update_last_activity
async def codes(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "codes": {
            "ru": "Отправьте 16-ти значный код для его активации 🔠",
            "en": "Send a 16-digit code to activate it 🔠"
        },
        "limit": {
            "ru": "Доступна только одна активация в сутки.",
            "en": "Only one activation per day is available."
        }
    }

    current_time: datetime = datetime.datetime.now()
    last_activate_time: datetime = users_table.get_last_activate(callback.from_user.id)[0]
    # 86401 - Заглушка для тех кто никогда не использовал промокоды.
    time_difference: datetime = 86401 if last_activate_time is None else (current_time - last_activate_time).total_seconds()

    # Check last activate time.
    if time_difference > 86400:
        await callback.answer(show_alert=False)
        await state.set_state(MainModuleStates.codes)

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "codes"),
            reply_markup=MainModule.modules["events"].keyboard_back(callback, "events"))
        return None
    else:
        await callback.answer(
            text=Translator.text(callback, strings, "limit"),
            show_alert=True)
        return None


@MainModule.router.message(StateFilter(MainModuleStates.codes))
@users_table.update_last_activity
async def code_handler(message: Message, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    code: list = codes_table.load_code(message.text)

    if len(code) != 0:
        strings: dict[str, dict] = {
            "success": {
                "ru": (f"Промокод успешно активирован ✅\n"
                       f"Вам начислено {code[0][2]} $tINCH."),
                "en": (f"Promo code successfully activated ✅\n"
                       f"You are credited with {code[0][2]} $tINCH.")
            }
        }

        data: dict = await state.get_data()
        await state.clear()

        users_table.activate_code(message.from_user.id, code[0][2])
        codes_table.delete_code(code[0][1])

        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data["events_message"],
            text=Translator.text(message, strings, "success"),
            reply_markup=MainModule.modules["events"].keyboard_close(message, "events"))
    else:
        strings: dict[str, dict] = {
            "fail": {
                "ru": "Недействительный промокод 🚫\n",
                "en": "Invalid promo code 🚫\n",
            }
        }

        await message.answer(
            text=Translator.text(message, strings, "fail"))

        await asyncio.sleep(3)

        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id+1)
    return None


# Slots -> ...
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
