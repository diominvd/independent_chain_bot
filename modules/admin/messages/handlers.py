import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.config import bot, users_table
from markdown import Markdown
from modules import AdminModuleStates
from modules.admin import AdminModule
from translator import Translator


@AdminModule.router.callback_query(F.data == "messages")
async def messages(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": f"{Markdown.bold('Список функций')}:\n"
                  f"• Личное сообщение - отправить личное сообщение пользователю от имени бота.\n"
                  f"• Рассылка - отправить массовую рассылку всем пользователям с последующим отчётом.",
            "en": f"{Markdown.bold('List of functions')}:\n"
                  f"• Private message - send a private message to the user on behalf of the bot.\n"
                  f"• Newsletter - send a mass newsletter to all users with a subsequent report.",
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.messages)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "description"),
        reply_markup=AdminModule.modules["messages"].keyboard(callback))
    return None


@AdminModule.router.callback_query(F.data == "mail")
async def mail(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": (f"Для отправки сообщения пользователю отправьте заполненный шаблон по данному примеру:\n\n"
                   f"{Markdown.monospaced('Имя пользователя # Текст сообщения # Текст кнопки # URL-адрес кнопки')}\n\n"
                   f"Если нет необходимости прикреплять кнопку к сообщению укажите последние два элемента как None."),
            "en": (f"To send a message to the user, send the completed template according to this example:\n\n"
                   f"{Markdown.monospaced('Username # The text of the message # Button text # Button url')}\n\n"
                   f"If there is no need to attach a button to a message, specify the last two elements as None.")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.mail)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "description"),
        reply_markup=AdminModule.modules["messages"].keyboard_cancel(callback, "messages"))
    return None


@AdminModule.router.message(StateFilter(AdminModuleStates.mail))
async def mail_content_handler(message: Message, state: FSMContext) -> None:
    content: list = message.text.split("#")

    username: str = content[0]
    mail_text: str = content[1]
    button_name: str = content[2]
    button_url: str = content[3]

    await bot.send_message(
        chat_id=users_table.get_value("user_id", "username", username),
        text=mail_text,
        reply_markup=AdminModule.modules["messages"].keyboard_mail_constructor(button_name, button_url))

    # Notify admin about send message.
    strings: dict[str, dict] = {
        "notify": {
            "ru": (f"Сообщение успешно отправлено ✉️\n"
                   f"{Markdown.bold('Получатель')}: @{username}\n"
                   f"{Markdown.bold('Текст сообщения')}: {mail_text}\n"
                   f"{Markdown.bold('Текст кнопки')}: {button_name}\n"
                   f"{Markdown.bold('URL кнопки')}: {button_url}\n"
                   f"{Markdown.bold('Время отправки')}: {datetime.datetime.now()}"),
            "en": (f"The message was sent successfully ✉️\n"
                   f"{Markdown.bold('Recipient')}: @{username}\n"
                   f"{Markdown.bold('Message text')}: {mail_text}\n"
                   f"{Markdown.bold('Button text')}: {button_name}\n"
                   f"{Markdown.bold('Button URL')}: {button_url}\n"
                   f"{Markdown.bold('Time of sending')}: {datetime.datetime.now()}")
        }
    }

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )

    data: dict = await state.get_data()
    panel_id: int = data["panel_id"]

    await bot.edit_message_text(
        text=Translator.text(message, strings, "notify"),
        chat_id=message.from_user.id,
        message_id=panel_id,
        reply_markup=AdminModule.modules["messages"].keyboard_close(message, "messages"))
    return None


@AdminModule.router.callback_query(F.data == "mailing")
async def mailing(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": (f"Для отправки рассылки отправьте заполненный шаблон по данному примеру:\n\n"
                   f"{Markdown.monospaced('Текст на русском языке # Текст RU кнопки # URL-адрес RU кнопки # Текст на английском языке # Текст EN кнопки # URL-адрес EN кнопки')}\n\n"
                   f"Если нет необходимости прикреплять кнопку к сообщению укажите текст кнопки и URL как None."),
            "en": (f"To send the mailing list, send the completed template according to this example:\n\n"
                   f"{Markdown.monospaced('Text in Russian # RU button text # RU button URL # English text # EN button text # EN button URL')}\n\n"
                   f"If there is no need to attach the button to the message, specify the button text and URL as None.")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminModuleStates.mailing)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "description"),
        reply_markup=AdminModule.modules["messages"].keyboard_cancel(callback, "messages"))
    return None


@AdminModule.router.message(StateFilter(AdminModuleStates.mailing))
async def mailing_content_handler(message: Message, state: FSMContext) -> None:
    content: list = message.text.split("#")

    ru_content: list = [content[0], content[1], content[2]]
    en_content: list = [content[3], content[4], content[5]]

    start_mailing_time: datetime = datetime.datetime.now()
    counter: dict = {"success": 0, "fail": 0}
    users: list = users_table.get_all_users_id()
    for user in users:
        try:
            user_language: str = users_table.get_value("language", "user_id", user)
            if user_language == "ru":
                await bot.send_message(
                    chat_id=user,
                    text=ru_content[0],
                    reply_markup=AdminModule.modules["messages"].keyboard_mail_constructor(ru_content[1],
                                                                                           ru_content[2]))
            else:
                await bot.send_message(
                    chat_id=user,
                    text=en_content[0],
                    reply_markup=AdminModule.modules["messages"].keyboard_mail_constructor(en_content[1],
                                                                                           en_content[2]))
        except:
            counter["fail"] += 1
        else:
            counter["success"] += 1

    # Notify admin about send mailing.
    end_mailing_time: datetime = datetime.datetime.now()
    strings: dict[str, dict] = {
        "notify": {
            "ru": (f"Рассылка успешно отправлено ✉️\n"
                   f"{Markdown.bold('Всего пользователей')}: {len(users)}\n"
                   f"{Markdown.bold('Успешно отправлено')}: {counter['success']}\n"
                   f"{Markdown.bold('Не отправлено')}: {counter['fail']}\n"
                   f"{Markdown.bold('Время рассылки')}: {(end_mailing_time - start_mailing_time).total_seconds()} секунд."),
            "en": (f"Newsletter successfully sent ✉️\n"
                   f"{Markdown.bold('Total users')}: {len(users)}\n"
                   f"{Markdown.bold('Successfully sent')}: {counter['success']}\n"
                   f"{Markdown.bold('Not sent')}: {counter['fail']}\n"
                   f"{Markdown.bold('Mailing time')}: {(end_mailing_time - start_mailing_time).total_seconds()} seconds.")
        }
    }

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )

    data: dict = await state.get_data()
    panel_id: int = data["panel_id"]

    await bot.edit_message_text(
        text=Translator.text(message, strings, "notify"),
        chat_id=message.from_user.id,
        message_id=panel_id,
        reply_markup=AdminModule.modules["messages"].keyboard_close(message, "messages"))
    return None
