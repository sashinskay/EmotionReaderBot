import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8000/predict"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Создаем клавиатуру с кнопками
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Текстовый анализ"),
            KeyboardButton(text="🎬 GIF-анализ")
        ]
    ],
    resize_keyboard=True
)

# Словарь с GIF-анимациями для разных эмоций
emotion_gifs = {
    "POSITIVE": "https://getfile.dokpub.com/yandex/get/https://disk.yandex.ru/i/SNt3YSnpfzG7aA",
    "NEGATIVE": "https://getfile.dokpub.com/yandex/get/https://disk.yandex.ru/i/ZkhpWTSMQtVr9Q",
    "NEUTRAL": "https://getfile.dokpub.com/yandex/get/https://disk.yandex.ru/i/K8qung4KckZTcg"
}

# Глобальная переменная для хранения выбранного режима
user_modes = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_modes[message.from_user.id] = "text"  # По умолчанию текстовый режим
    await message.answer(
        "Привет!\n "
        "Я могу анализировать эмоциональную окраску текста.\n"
        "Выбери формат ответа:",
        reply_markup=start_keyboard
    )

@dp.message_handler(lambda message: message.text == "📝 Текстовый анализ")
async def enable_text_mode(message: types.Message):
    user_modes[message.from_user.id] = "text"
    await message.answer("Режим текстового анализа активирован. \nПросто отправь мне текст!")

@dp.message_handler(lambda message: message.text == "🎬 GIF-анализ")
async def enable_gif_mode(message: types.Message):
    user_modes[message.from_user.id] = "gif"
    await message.answer("Режим GIF-анализа активирован. \nПросто отправь мне текст!")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def analyze_text(message: types.Message):
    # Пропускаем команды и кнопки
    if message.text in ["📝 Текстовый анализ", "🎬 GIF-анализ"]:
        return

    user_id = message.from_user.id
    current_mode = user_modes.get(user_id, "text")  # По умолчанию текстовый режим

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={"text": message.text}) as resp:
            if resp.status == 200:
                data = await resp.json()
                label = data["label"]
                score = data["score"]
                
                # Определяем эмодзи и GIF
                if label == "POSITIVE":
                    emoji = "😊"
                    gif = emotion_gifs["POSITIVE"]
                elif label == "NEGATIVE":
                    emoji = "😠"
                    gif = emotion_gifs["NEGATIVE"]
                else:
                    emoji = "😐"
                    gif = emotion_gifs["NEUTRAL"]
                
                response_text = (
                    f"Эмоциональная окраска: {label} {emoji}\n"
                    f"Уверенность: {score:.2f}"
                )
                
                # Отправляем ответ в выбранном формате
                if current_mode == "gif":
                    try:
                        await message.answer_animation(
                            animation=gif,
                            caption=response_text
                        )
                    except Exception as e:
                        logging.error(f"Ошибка отправки GIF: {e}")
                        await message.answer("Не удалось отправить GIF, вот текстовый анализ:\n\n" + response_text)
                else:
                    await message.answer(response_text)
            else:
                await message.answer("Ошибка анализа 😢")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)