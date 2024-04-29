from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.wallet_kb import wallet_kb
from states import BotStates
from utils.translator import translate


@callback_router.callback_query(F.data == "wallet")
@database.update_activity
async def support_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotStates.waiting_wallet)
    strings: dict[str, dict] = {
        "no_wallet_request": {
            "ru": f"Отправьте адрес кошелька в чат с ботом Ton Space, чтобы привязать его к профилю.",
            "en": f"Send the wallet address to the chat with the Ton Space bot to link it to your profile."
        },
        "yes_wallet_request": {
            "ru": f"К вашему профилю уже привязан адрес кошелька Ton Space. Чтобы привязать новый - отправьте адрес "
                  f"кошелька Ton Space в чат с ботом.",
            "en": f"The Ton Space wallet address is already linked to your profile. To link a new one, send the "
                  f"Ton Space wallet address to the chat with bot."
        }
    }

    await callback.answer(show_alert=False)
    # Check user wallet existence.
    if database.get_wallet(user_id=callback.from_user.id) is None:
        request_text: str = translate(callback, strings["no_wallet_request"])
    else:
        request_text: str = translate(callback, strings["yes_wallet_request"])

    await callback.message.edit_text(
        text=request_text,
        reply_markup=wallet_kb(callback)
    )
    return None

