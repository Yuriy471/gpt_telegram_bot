import os
import logging
import asyncio
import threading
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from http.server import BaseHTTPRequestHandler, HTTPServer
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка на ошибки
if TELEGRAM_BOT_TOKEN is None or OPENAI_API_KEY is None:
    raise ValueError("❌ Проверь, что переменные TELEGRAM_BOT_TOKEN и OPENAI_API_KEY указаны в .env!")

# Инициализация бота
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Инициализация OpenAI клиента
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Обработчик сообщений
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

# HTTP-сервер для Render (порт 8080)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_healthcheck_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

# Асинхронный запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_healthcheck_server, daemon=True).start()
    asyncio.run(main())