# app/telegram_notifier.py

import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def escape_markdown(text: str) -> str:
    """
    Escapes special characters in text for Telegram MarkdownV2.
    """
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": escape_markdown(message),
        "parse_mode": "MarkdownV2",  # Ensures escaped text is interpreted safely
        "disable_web_page_preview": True
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Telegram error {response.status_code}: {response.text}")
    else:
        print("✅ Message sent to Telegram successfully!")
