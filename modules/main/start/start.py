from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import UsersTable
from markdown import Markdown
from modules.main import MainModule
from translator import Translator


def language(language_code: str) -> str:
    if language_code not in ["ru", "en"]:
        return "en"
    else:
        return language_code


def inviter(message: Message) -> int | None:
    text: list = message.text.split(" ")
    if len(text) == 2:
        inviter_id: int = int(text[1])
        return inviter_id
    else:
        return None


@MainModule.router.message(F.chat.type == ChatType.PRIVATE, Command("start"))
async def start_(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "greeting": {
            "ru": (
                f"Добро пожаловать в {Markdown.bold('INCH Project')} - крипто-проект, запущенный группой энтузиастов.\n\n"
                f"Наша цель - запустить собственную, независимую от коммерческих организаций, спонсоров и сторонних "
                f"организаций блокчейн-сеть с внутресетевой монетой.\n\n"
                f"Уже запущена рекламная компания на платформе Telegram в рамках которой было отчеканено 10,000,000 "
                f"жетонов $INCH в сети TON 🔥\n\n"
                f"За каждого приглашённого друга вы получите 50 $tINCH - внутрення валюта бота. В дальнейшем каждый "
                f"сможет конвертировать свои накопления в жетон $INCH 🔄\n\n"
                f"Для просмотра профиля воспользуйтесь командой /profile."),
            "en": (
                f"Welcome to {Markdown.bold('INCH Project')}, a crypto project launched by a group of enthusiasts.\n\n"
                f"Our goal is to launch our own blockchain network with an intra-network coin, independent of commercial "
                f"organizations, sponsors and third-party organizations.\n\n"
                f"An advertising campaign has already been launched on the Telegram platform, within the framework of which 10,000,000 "
                f"$INCH tokens were minted on the TON 🔥\n\n network"
                f"For each invited friend, you will receive $ 50 tINCH - the internal currency of the bot. In the future, everyone "
                f"will be able to convert his savings into a $INCH token 🔄\n\n"
                f"To view the profile, use the /profile command.")
        }
    }

    await state.clear()

    # Check user existence in bot database.
    user: tuple = UsersTable.select(("user_id", ), "user_id", message.from_user.id)
    if user is None:
        UsersTable.insert(
            user_id=message.from_user.id,
            username=message.from_user.username,
            language=language(message.from_user.language_code),
            wallet="NULL",
            balance=UsersTable.start,
            referals=0
        )

    inviter_id: int | None = inviter(message)
    if inviter_id is not None:
        UsersTable.increase("referals", 1, "user_id", message.from_user.id)
        UsersTable.increase("balance", UsersTable.referal, "user_id", inviter_id)

    await message.answer_photo(
        photo="https://github.com/diominvd/independent_chain_bot/blob/main/modules/main/start/image.jpg?raw=true",
        caption=Translator.text(message, strings, "greeting"),
        reply_markup=MainModule.modules["start"].keyboard(message))
