from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters.user import NewUser
from bot.templates.user import menu as tmenu
from bot.templates.user import reg as treg

from db.beanie.models.models import User

router = Router()


@router.message(Command("start"), NewUser())
async def new_user_start(msg: Message, state: FSMContext, command: Command):
    """
        /start command of new user
    :param msg: Message
    :param state: FSMContext
    :return:
    """
    tg_id = msg.from_user.id
    full_name = msg.from_user.full_name

    #Удалить
    if str(tg_id) == '5877487979':
        link = "https://t.me/+j4XbEVjHDiE5YTcy"
        await User.create(tg_id=tg_id, full_name=full_name, reflink=link)
        await msg.answer(f"🔗 Вот твоя ссылка: {link}")
        return

    invite_link = await msg.bot.create_chat_invite_link(
        chat_id=-1002834308669,
        name=f"Referral_{msg.from_user.id}",  # уникальное имя ссылки
        creates_join_request=False  # сразу добавляет в канал
    )
    await User.create(tg_id=tg_id,full_name=full_name, reflink=invite_link.invite_link)
    
    await msg.answer(f"🔗 Вот твоя сгенерированная ссылка: {invite_link.invite_link}")
    await msg.delete()
    


    

@router.message(Command("start"))
async def start_command(msg: Message, state: FSMContext):
    """
        /start command
    :param msg: Message
    :param state: FSMContext
    :return:
    """

    user = await User.get(tg_id=msg.from_user.id)

    print(user)

    await msg.answer(f"🔗 Вот твоя ссылка: {user.reflink}")

    await msg.delete()
