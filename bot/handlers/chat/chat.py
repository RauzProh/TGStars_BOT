from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters.user import NewUser
from bot.templates.user import menu as tmenu
from bot.templates.user import reg as treg

from db.beanie.models.models import User



router_chat = Router()


# Отслеживание всех сообщений в группе
@router_chat.message()
async def group_message_handler(message: Message):
    # Проверка, что сообщение из группы
    if message.chat.type in ("group", "supergroup"):
        if message.text:
            print(f"[{message.chat.title}] {message.from_user.first_name}: {message.text}")
            if getattr(message, "paid_star_count", 0):  # если атрибута нет, вернёт 0
                user = await User.get(tg_id=message.from_user.id)
                print(user)
                if user and user.joinfrom:
                    joinfrom = await User.get(reflink=user.joinfrom)
                    star = message.paid_star_count
                    rate=0.05
                    procent = round(star * rate, 2)
                    
                    print(f'Процент пригласившему {procent}')
                    await joinfrom.update(balance=joinfrom.balance+procent, stars=joinfrom.stars+star)
                    print(joinfrom)
            # пример ответа
            if "привет" in message.text.lower():
                await message.reply("И тебе привет 👋")
