import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBVIEW_URL = os.getenv("WEBVIEW_URL", "https://example.com")

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN is not set.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

translations = {
    "welcome": {
        "ru": "👋 Добро пожаловать! Нажмите START, чтобы получить бонус.",
        "en": "👋 Welcome! Tap START to claim your bonus.",
        "fr": "👋 Bienvenue ! Appuyez sur START pour réclamer votre bonus."
    },
    "cta_title": {
        "ru": "🎁 Ваш специальный бонус готов!",
        "en": "🎁 Your special bonus is ready!",
        "fr": "🎁 Votre bonus spécial est prêt !"
    },
    "cta_button": {
        "ru": "Получить сейчас",
        "en": "Claim now",
        "fr": "Obtenez-le maintenant"
    }
}

def tr(key, lang):
    lang = (lang or "en").split("-")[0]
    if lang not in ("ru", "en", "fr"):
        lang = "en"
    return translations.get(key, {}).get(lang, translations[key]["en"])

@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    lang = message.from_user.language_code or "en"
    text = tr("welcome", lang) + "\n\n" + tr("cta_title", lang)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(tr("cta_button", lang), url=WEBVIEW_URL))
    await message.answer(text, reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
