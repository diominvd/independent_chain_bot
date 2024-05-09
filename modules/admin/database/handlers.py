from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.config import users_table, mining_table, bot
from markdown import Markdown
from modules import AdminModuleStates
from modules.admin import AdminModule
from translator import Translator


@AdminModule.router.callback_query(F.data == "database")
async def database(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": f"{Markdown.bold('Список функций')}:\n"
                  f"• Статистика - просмотр статистики бота.\n"
                  f"• Получить значение - запрос к базе данных.\n"
                  f"• Изменить значение - изменить внутреннее значение бота.",
            "en": f"{Markdown.bold('List of functions')}:\n"
                  f"• Statistics - view the statistics of the bot.\n"
                  f"• Get a value - query the database.\n"
                  f"• Change value - change the internal value of the bot."
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.database)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "description"),
        reply_markup=AdminModule.modules["database"].keyboard(callback))
    return None


# Statistics ->...
@AdminModule.router.callback_query(StateFilter(AdminModuleStates.database), F.data == "statistics")
async def database(callback: CallbackQuery, state: FSMContext) -> None:
    query: str = "SELECT COUNT(user_id) FROM users"
    users: int = users_table.select(query, ())[0][0]

    query: str = "SELECT COUNT(user_id) FROM mining"
    miners: int = mining_table.select(query, ())[0][0]

    query: str = "SELECT SUM(balance) FROM users"
    balances: float = round(users_table.select(query, ())[0][0], 4)

    strings: dict[str, dict] = {
        "statistics": {
            "ru": f"{Markdown.bold('Статистика Independent Chain Bot')} 📊\n\n"
                  f"{Markdown.bold('Всего пользователей')}: {users}\n"
                  f"{Markdown.bold('Всего майнеров')}: {miners}\n"
                  f"{Markdown.bold('Добыто монет')}: {balances}\n",
            "en": f"{Markdown.bold('Independent Chain Bot statistics')} 📊\n\n"
                  f"{Markdown.bold('Total users')}: {users}\n"
                  f"{Markdown.bold('Total miners')}: {miners}\n"
                  f"{Markdown.bold('Coins mined')}: {balances}\n",
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.statistics)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "statistics"),
        reply_markup=AdminModule.modules["database"].keyboard_back(callback, "database"))
    return None


# Get Values -> ...
@AdminModule.router.callback_query(StateFilter(AdminModuleStates.database, AdminModuleStates.get_values),
                                   F.data == "get_values")
async def get_values(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "information": {
            "ru": (f"{Markdown.bold('Список доступных таблиц и полей')} 🗂\n\n"
                   f"• users - Основная таблица с данными пользователей.\n"
                   f"-- registration\n"
                   f"-- last_activity\n"
                   f"-- language\n"
                   f"-- project_id\n"
                   f"-- user_id\n"
                   f"-- user_id\n"
                   f"-- inviter_id\n"
                   f"-- username\n"
                   f"-- balance\n"
                   f"-- referals\n\n"
                   f"• mining - Таблица с данными майнеров.\n"
                   f"-- user_id\n"
                   f"-- last_claim\n"
                   f"-- booster\n"
                   f"-- claims\n"
                   f"-- amount\n\n"
                   f"Для получения значения отправьте заполненный шаблон по данному примеру:\n\n"
                   f"{Markdown.monospaced('название таблицы:параметр:название фильтра:значение фильтра:тип значения (str, int, float)')}"),
            "en": (f"{Markdown.bold('List of available tables and fields')} 🗂\n\n"
                   f"• users - The main table with user data.\n"
                   f"-- registration\n"
                   f"-- last_activity\n"
                   f"-- language\n"
                   f"-- project_id\n"
                   f"-- user_id\n"
                   f"-- user_id\n"
                   f"-- inviter_id\n"
                   f"-- username\n"
                   f"-- balance\n"
                   f"-- referals\n\n"
                   f"• mining - A table with miner data.\n"
                   f"-- user_id\n"
                   f"-- last_claim\n"
                   f"-- booster\n"
                   f"-- claims\n"
                   f"-- amount\n\n"
                   f"To get the value, send the completed template according to this example:\n\n"
                   f"{Markdown.monospaced('table name:parameter:name of the filter:filter value:value type (str, int, float)')}")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.get_values)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "information"),
        reply_markup=AdminModule.modules["database"].keyboard_back(callback, "database"))
    return None


@AdminModule.router.message(StateFilter(AdminModuleStates.get_values))
async def get_values_handler(message: Message, state: FSMContext) -> None:
    content: list = message.text.split(":")
    value: any = AdminModule.modules["database"].get_value(content)

    strings: dict[str, dict] = {
        "response": {
            "ru": (f"{Markdown.bold('Отчёт по запросу')} 📥\n\n"
                   f"{Markdown.bold('Таблица')}: {content[0]}\n"
                   f"{Markdown.bold('Параметр')}: {content[1]}\n"
                   f"{Markdown.bold('Фильтр')}: {content[2]}\n"
                   f"{Markdown.bold('Значение фильтра')}: {content[3]}\n"
                   f"{Markdown.bold('Ответ')}: {value}"),
            "en": (f"{Markdown.bold('Report on request')} 📥\n\n"
                   f"{Markdown.bold('Table')}: {content[0]}\n"
                   f"{Markdown.bold('Parameter')}: {content[1]}\n"
                   f"{Markdown.bold('Filter')}: {content[2]}\n"
                   f"{Markdown.bold('Filter value')}: {content[3]}\n"
                   f"{Markdown.bold('Response')}: {value}"),
        }
    }

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    data: dict = await state.get_data()
    panel_id: int = data["panel_id"]

    await bot.edit_message_text(
        text=Translator.text(message, strings, "response"),
        chat_id=message.from_user.id,
        message_id=panel_id,
        reply_markup=AdminModule.modules["database"].keyboard_close(message, "get_values"))
    return None


# Change Values ->...
@AdminModule.router.callback_query(StateFilter(AdminModuleStates.database, AdminModuleStates.change_values),
                                   F.data == "change_values")
async def change_values(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "information": {
            "ru": (f"{Markdown.bold('Список доступных значений')} 🔢\n\n"
                   f"• start_reward ({users_table.start_reward}) - Награда за регистрацию в боте.\n"
                   f"• referal_reward ({users_table.referal_reward}) - Награда за приглашённого пользователя.\n"
                   f"• global_booster ({mining_table.global_booster}) - Общий усилитель добычи.\n\n"
                   f"Для изменения значения отправьте заполненный шаблон по данному примеру:\n"
                   f"{Markdown.monospaced('название=значение')}"),
            "en": (f"{Markdown.bold('List of available values')} 🔢\n\n"
                   f"• start_reward - Reward for registering in the bot.\n"
                   f"• referal_reward - Reward for the invited user.\n"
                   f"• global_booster is a general mining booster.\n\n"
                   f"To change the value, send the completed template according to this example:\n"
                   f"{Markdown.monospaced('name=value')}")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.change_values)

    try:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "information"),
            reply_markup=AdminModule.modules["database"].keyboard_back(callback, "database"))
    except Exception as e:
        print(e)
    return None


@AdminModule.router.message(StateFilter(AdminModuleStates.change_values))
async def change_values_handler(message: Message, state: FSMContext) -> None:
    content: list = message.text.split("=")
    name: str = content[0]
    value: float = float(content[1])

    AdminModule.modules["database"].change_value(name, value)

    strings: dict[str, dict] = {
        "response": {
            "ru": (f"{Markdown.bold('Значение изменено')} 📤\n\n"
                   f"{Markdown.bold('Имя значения')}: {name}\n"
                   f"{Markdown.bold('Значение')}: {value}\n\n"
                   f"Открыть панель управления: /admin"),
            "en": (f"{Markdown.bold('Value changed')} 📤\n\n"
                   f"{Markdown.bold('Value Name')}: {name}\n"
                   f"{Markdown.bold('Value')}: {value}\n\n"
                   f"Open the control panel: /admin")
        }
    }

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    data: dict = await state.get_data()
    panel_id: int = data["panel_id"]

    await bot.edit_message_text(
        text=Translator.text(message, strings, "response"),
        chat_id=message.from_user.id,
        message_id=panel_id,
        reply_markup=AdminModule.modules["database"].keyboard_close(message, "change_values"))
    return None
