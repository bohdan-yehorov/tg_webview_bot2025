import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBVIEW_URL = os.getenv("WEBVIEW_URL", "https://example.com")

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN is not set.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# переклади для EN / FR / RU
MESSAGES = {
    "en": {
        "cta_title": "🎁 Your special bonus is ready!",
        "cta_button": "Open Bonus",
    },
    "fr": {
        "cta_title": "🎁 Votre bonus spécial est prêt !",
        "cta_button": "Ouvrir le bonus",
    },
    "ru": {
        "cta_title": "🎁 Ваш специальный бонус готов!",
        "cta_button": "Открыть бонус",
    },
}

def tr(key: str, lang: str):
    lang = (lang or "en").split("-")[0]
    if lang not in ("en", "fr", "ru"):
        lang = "en"
    return MESSAGES[lang][key]

@dp.message_handler(commands=["start", "help"])
async def start_cmd(message: types.Message):
    lang = (message.from_user.language_code or "en").split("-")[0]
    if lang not in ("en", "fr", "ru"):
        lang = "en"

    text = tr("cta_title", lang)

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text=tr("cta_button", lang),
            web_app=WebAppInfo(url=WEBVIEW_URL)
        )
    )

    await message.answer(text, reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
