import asyncio
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import random

# Токен вашего бота
TOKEN = "9030023964:AAELwPjwPKvnDNpSQ6rP6fTGkOyCuz3L0Ho"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения загаданных чисел игроков
user_games = {}

@dp.message(Command("start", "game"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_games[user_id] = random.randint(1, 100)
    await message.answer(
        "🎲 Я загадал число от 1 до 100!\nПопробуй угадать его. Напиши свое число:"
    )

@dp.message()
async def guess_number(message: types.Message):
    user_id = message.from_user.id
    
    # Если бот запущен заново, а игра не начата
    if user_id not in user_games:
        user_games[user_id] = random.randint(1, 100)
        await message.answer("Я загадал число от 1 до 100! Попробуй угадать:")
        return

    try:
        guess = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите целое число от 1 до 100.")
        return

    secret_number = user_games[user_id]

    if guess < secret_number:
        await message.answer("📈 Мое число **больше**! Попробуй еще раз.")
    elif guess > secret_number:
        await message.answer("📉 Мое число **меньше**! Попробуй еще раз.")
    else:
        await message.answer(
            f"🎉 Поздравляю! Ты угадал число **{secret_number}**!\n"
            "Хочешь сыграть еще? Просто отправь /game"
        )
        # Загадываем новое число для следующей игры
        user_games[user_id] = random.randint(1, 100)

# Мини-сервер для Render (обязателен для прохождения проверки порта)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Запускаем веб-сервер в отдельном потоке
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    # Запуск бота
    asyncio.run(main())
