import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()

# Получение токенов
TELEGRAM_BOT_TOKEN = "7761613384:AAHuAV0zOrC3ToRMOij3BCgpjUnrV55ZeXA"
OPENAI_API_KEY = "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"

# Проверка токенов
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Переменные TELEGRAM_BOT_TOKEN и OPENAI_API_KEY не найдены. Проверь .env или Render → Environment.")

# Логирование
logging.basicConfig(level=logging.INFO)

# Настройка Telegram бота
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Инициализация OpenAI
openai_client = OpenAI(api_key=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)

# Обработка входящих сообщений
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

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())