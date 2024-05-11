from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table, geckoshi_table, bot
from markdown import Markdown
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "geckoshi")
@users_table.update_last_activity
async def geckoshi(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "geckoshi": {
            "ru": (f"Подпишитесь на канал наших официальных партнёров {Markdown.monospaced('Geckoshi')} 🦎\n\n"
                   f"Geckoshi является первой инвестиционной мем-монетой. В планах проекта - использовать $GMEME в "
                   f"своё основном проекте после firelaunch 🔥\n\n"
                   f"{Markdown.bold('Награда за подписку')}: 200 $tINCH."),
            "en": (f"Subscribe to the channel of our official partners {Markdown.monospaced('Geckoshi')} 🦎\n\n"
                   f"Geckoshi is the first investment meme coin. The project plans to use $GMEME in "
                   f"your main project after firelaunch 🔥\n\n"
                   f"{Markdown.bold('Subscription Reward')}: 200 $tINCH.")
        },
        "completed": {
            "ru": "Это задание уже выполнено 🦎",
            "en": "This task has already been completed 🦎"
        }
    }

    if geckoshi_table.check_user(callback.from_user.id):
        await callback.answer(
            text=Translator.text(callback, strings, "completed"),
            show_alert=True)
    else:
        await state.set_state(MainModuleStates.geckoshi)

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "geckoshi"),
            reply_markup=MainModule.modules["events"].keyboard_geckoshi(callback))
    return None


@MainModule.router.callback_query(StateFilter(MainModuleStates.geckoshi), F.data == "check_subscribe")
@users_table.update_last_activity
async def check_subscribe(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "success": {
            "ru": "Спасибо за подписку!\n"
                  "200 $tINCH начислены на ваш счёт.",
            "en": "Thanks for subscribing!\n"
                  "$200 tINCH has been credited to your account."
        },
        "fail": {
            "ru": "Вы не подписаны на канал.",
            "en": "You are not subscribed to the channel."
        }
    }

    try:
        user_channel_status = await bot.get_chat_member(chat_id='@geckoshi_coin', user_id=callback.from_user.id)
    except:
        pass
    else:
        if user_channel_status.status != 'left':
            geckoshi_table.create_user(callback.from_user.id)
            users_table.update_balance(callback.from_user.id, "+", 200)

            await state.clear()

            await callback.answer(
                text=Translator.text(callback, strings, "success"),
                show_alert=True)

            await MainModule.modules["events"].events(callback, state)
        else:
            await callback.answer(
                text=Translator.text(callback, strings, "fail"),
                show_alert=True)
    return None