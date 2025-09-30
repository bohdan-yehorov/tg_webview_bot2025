import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBVIEW_URL = os.getenv("WEBVIEW_URL", "https://example.com")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

translations = {
    "welcome": {
        "ru": "👋 Добро пожаловать! Нажмите START, чтобы получить бонус.",
        "en": "👋 Welcome! Tap START to claim your bonus.",
        "fr": "👋 Bienvenue ! Appuyez sur START pour réclamer votre bonus."
    },
    "start_title": {
        "ru": "🎁 Ваш специальный бонус готов!",
        "en": "🎁 Your special bonus is ready!",
        "fr": "🎁 Votre bonus spécial est prêt!"
    },
    "start_button": {
        "ru": "Получить сейчас",
        "en": "Claim now",
        "fr": "Obtenez-le maintenant"
    }
}

def t(key, lang):
    if lang not in ["ru", "en", "fr"]:
        lang = "en"
    return translations.get(key, {}).get(lang, "")

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    lang = message.from_user.language_code
    if lang not in ["ru", "en", "fr"]:
        lang = "en"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=t("start_button", lang), url=WEBVIEW_URL))

    text = t("welcome", lang) + "\n\n" + t("start_title", lang)
    await message.answer(text, reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
