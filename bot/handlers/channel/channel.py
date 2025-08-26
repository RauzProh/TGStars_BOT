from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters.user import NewUser
from bot.templates.user import menu as tmenu
from bot.templates.user import reg as treg

from db.beanie.models.models import User

router_channel = Router()


@router_channel.chat_member()
async def track_join(event: types.ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        if event.invite_link:
            await event.bot.send_message(
                event.chat.id,
                f"{event.from_user.full_name} присоединился по ссылке: {event.invite_link.invite_link}"
            )


            user = await User.get(reflink = event.invite_link.invite_link)
            if user:
                await User.create(tg_id=event.from_user.id, joinfrom=event.invite_link.invite_link)
                print('Реферал создан')
                print(user)
                