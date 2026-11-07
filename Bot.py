import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
TOKEN = "9030023964:AAELwPjwPKvnDNpSQ6rP6fTGkOyCuz3L0Ho"
bot = Bot(token=TOKEN)
dp = Dispatcher()
class GameStates(StatesGroup):
    playing = State()
user_data = {}
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    """Приветствие и правила игры"""
    await state.clear()
    await message.answer(
        "Привет! 👋 Я загадал число от 1 до 100.\n"
        "Попробуй угадать его!\n\n"
        "Просто отправь мне число, а я подскажу, больше оно или меньше.\n"
        "Для сброса или начала новой игры отправь команду /game"
    )
@dp.message(Command("game"))
async def cmd_game(message: types.Message, state: FSMContext):
    """Начало новой игры"""
    secret_number = random.randint(1, 100)
    user_data[message.from_user.id] = secret_number
    
    await state.set_state(GameStates.playing)
    await message.answer(
        "🎮 Я загадал новое число от 1 до 100. Жду твою первую попытку!"
    )
@dp.message(GameStates.playing, F.text)
async def process_guess(message: types.Message, state: FSMContext):
    """Обработка попытки пользователя угадать число"""
    user_id = message.from_user.id
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите целое число от 1 до 100.")
        return
    guess = int(message.text)
    secret_number = user_data.get(user_id)
    if secret_number is None:
        secret_number = random.randint(1, 100)
        user_data[user_id] = secret_number
    if guess < secret_number:
        await message.answer("📈 Мое число **больше**! Попробуй еще раз.")
    elif guess > secret_number:
        await message.answer("📉 Мое число **меньше**! Попробуй еще раз.")
    else:
        await message.answer(
            f"🎉 Поздравляю! Ты угадал число **{secret_number}**!\n"
            "Хочешь сыграть еще? Просто отправь /game"
        )
        await state.clear()
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
