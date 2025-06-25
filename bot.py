import re
import logging
from aiogram import Bot, Dispatcher, executor, types
import os

TOKEN = os.getenv("BOT_TOKEN")  # токен из переменной окружения
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # ID админа из переменной окружения

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Отправь своё объявление, я передам его администратору на проверку.\n\n"
        "📋 Вот пример правильного формата объявления:\n"
        "🐾 Отдам котёнка 1,5 месяца, здоров, кушает самостоятельно.\n"
        "📍 Город: Киров\n"
        "📞 Контакт для связи: @username или телефон\n\n"
        "Постарайся писать кратко и понятно, чтобы быстрее найти нового хозяина!"
    )

def contains_contact(text: str) -> bool:
    if re.search(r'@\w{5,}', text):
        return True
    if re.search(r'(\+?\d[\d\s\-]{5,}\d)', text):
        return True
    return False

@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_ad_to_admin(message: types.Message):
    if message.chat.type != 'private':
        return

    if message.content_type == 'text':
        if not contains_contact(message.text):
            await message.answer(
                "⚠️ Пожалуйста, укажи в объявлении контакт — это может быть Telegram @username или номер телефона.\n"
                "Попробуй ещё раз."
            )
            return

    await message.forward(ADMIN_ID)
    await message.answer("Спасибо! Твоё объявление отправлено на проверку.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
