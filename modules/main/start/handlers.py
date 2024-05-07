from aiogram.filters import Command
from aiogram.types import Message

from modules.main import MainModule
from core.config import users_table
from markdown import Markdown
from utils import translate


@MainModule.router.message(Command("start"))
async def start(message: Message) -> None:
    strings: dict[str, dict] = {
        "greeting": {
            "ru": f"Добро пожаловать в {Markdown.bold('INCH Project')} - крипто-проект, запущенный группой энтузиастов.\n\n"
                  f"Наша цель - запустить собственную, независимую от коммерческих организаций, спонсоров и сторонних "
                  f"организаций блокчейн-сеть с внутресетевой монетой.\n\n"
                  f"Уже запущена рекламная компания на платформе Telegram в рамках которой было отчеканено 10,000,000 "
                  f"жетонов $INCH в сети TON 🔥\n\n"
                  f"За каждого приглашённого друга вы получите 50 $tINCH - внутрення валюта бота. В дальнейшем каждый "
                  f"сможет конвертировать свои накопления в жетон $INCH 🔄\n\n"
                  f"Для просмотра профиля воспользуйтесь командой /profile.",
            "en": f"Welcome to {Markdown.bold('INCH Project')}, a crypto project launched by a group of enthusiasts.\n\n"
                  f"Our goal is to launch our own blockchain network with an intra-network coin, independent of commercial "
                  f"organizations, sponsors and third-party organizations.\n\n"
                  f"An advertising campaign has already been launched on the Telegram platform, within the framework of which 10,000,000 "
                  f"$INCH tokens were minted on the TON 🔥\n\n network"
                  f"For each invited friend, you will receive $ 50 tINCH - the internal currency of the bot. In the future, everyone "
                  f"will be able to convert his savings into a $INCH token 🔄\n\n"
                  f"To view the profile, use the /profile command."
        }
    }

    # Check user existence in bot database.
    user_existence: bool = users_table.check_user(user_id=message.from_user.id)
    if not user_existence:
        user_data: dict = MainModule.modules["start"].pack_user_data(message)
        users_table.create_user(user_data)

    # Answer message.
    await message.answer(
        text=translate(message, strings, "greeting"),
        reply_markup=MainModule.modules["start"].keyboard(message)
    )
    return None
