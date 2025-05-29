# app/test_telegram.py

from telegram_notifier import send_telegram_message

if __name__ == "__main__":
    send_telegram_message("Hey AK! 🚀 Telegram messaging from Docker is working!")
