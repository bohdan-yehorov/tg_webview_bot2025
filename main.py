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

# переклади
MESSAGES = {
    "en": {
        "cta_button": "Open Bonus",
    },
    "fr": {
        "cta_button": "Ouvrir le bonus",
    },
    "uk": {
        "cta_button": "Відкрити бонус",
    },
    "ru": {
        "cta_button": "Открыть бонус",
    },
}

def tr(key: str, lang: str):
    return MESSAGES.get(lang, MESSAGES["en"]).get(key, key)

@dp.message_handler(commands=["start", "help"])
async def start_cmd(message: types.Message):
    lang = (message.from_user.language_code or "en").split("-")[0]

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text=tr("cta_button", lang),
            web_app=WebAppInfo(url=WEBVIEW_URL)
        )
    )

    await message.answer(tr("cta_button", lang), reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
