from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile
from io import BytesIO
import pandas as pd

from bot.filters.admin import IsAdmin
from bot.templates.admin import menu as tmenu
from db.beanie.models.models import User  # импорт модели User

router = Router()
router.message.filter(IsAdmin())

@router.message(Command("export_users"))
async def export_users(msg: Message):
    # Получаем всех пользователей из БД
    users = await User.all()

    # Формируем список словарей
    data = []
    for u in users:
        data.append({
            "tg_id": u.tg_id,
            "full_name": u.full_name,
            "reflink": u.reflink,
            "joinfrom": u.joinfrom,
            "balance": u.balance,
            "stars": u.stars,
            "created_at": u.created_at
        })

    # Создаем DataFrame
    df = pd.DataFrame(data)

    # Сохраняем в Excel в память
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    # Создаем BufferedInputFile для отправки
    file = BufferedInputFile(buffer.read(), filename="users.xlsx")

    # Отправляем файл администратору
    await msg.answer_document(file)
    await msg.delete()
