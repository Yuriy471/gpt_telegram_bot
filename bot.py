import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from openai import OpenAI
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка переменных
if TELEGRAM_BOT_TOKEN is None or OPENAI_API_KEY is None:
    raise ValueError("❌ Проверь .env файл: отсутствуют TELEGRAM_BOT_TOKEN или OPENAI_API_KEY")

# Инициализация бота
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Инициализация OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Обработка сообщений
@router.message()
async def handle_message(message: types.Message):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник."},
                {"role": "user", "content": message.text}
            ]
        )
        answer = response.choices[0].message.content.strip()
        await message.answer(answer)
    except Exception as e:
        logging.error(f"Ошибка GPT: {e}", exc_info=True)
        await message.answer(f"⚠️ Ошибка: {e}")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())