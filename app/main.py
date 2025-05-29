import os
import logging
import re
from flask import Flask
from email_reader import fetch_unread_emails
from summarizer import summarize_email
from dotenv import load_dotenv
from telegram import Bot
from email.utils import parsedate_to_datetime

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Telegram Bot setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

SEPARATOR = "\n**************************************************************************\n"
MAX_MSG_LENGTH = 4000

def escape_markdown(text):
    """Escape Telegram Markdown special characters."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(rf'([{re.escape(escape_chars)}])', r'\\\1', text)

def send_telegram_message(text):
    """Send safely escaped message to Telegram."""
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="MarkdownV2")
    except Exception as e:
        logging.error(f"Telegram error: {e}")

def split_and_send(summary_text):
    """Chunk and send long messages safely to Telegram."""
    chunks = summary_text.split(SEPARATOR)
    current_msg = ""

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        next_block = chunk + f"\n{SEPARATOR}\n"
        if len(current_msg) + len(next_block) < MAX_MSG_LENGTH:
            current_msg += next_block
        else:
            send_telegram_message(escape_markdown(current_msg.strip()))
            current_msg = next_block

    if current_msg:
        send_telegram_message(escape_markdown(current_msg.strip()))

@app.route("/trigger", methods=["GET"])
def trigger_summarizer():
    try:
        emails = fetch_unread_emails()
        if not emails:
            send_telegram_message("📭 No new unread emails found.")
            return "No new emails found.", 200

        summary_text = ""
        for email in emails:
            subject = email.get("subject", "No Subject")
            sender = email.get("from", "Unknown Sender")
            raw_date = email.get("date", "Unknown Date")
            body = email.get("body", "")

            try:
                parsed_date = parsedate_to_datetime(raw_date)
                formatted_date = parsed_date.strftime("%a, %d %b %Y %I:%M %p")
            except Exception as e:
                logging.warning(f"Failed to parse date '{raw_date}': {e}")
                formatted_date = raw_date

            logging.info(f"Summarizing email from {sender}...")
            summary = summarize_email(body)

            entry = (
                f"📧 *From:* {sender}\n"
                f"📝 *Subject:* {subject}\n"
                f"📅 *Date:* {formatted_date}\n"
                f"🧠 *Summary:*\n{summary.strip()}\n"
                f"{SEPARATOR}\n"
            )
            summary_text += entry

        split_and_send(summary_text)
        return "Summarization sent to Telegram.", 200

    except Exception as e:
        logging.error(f"Error occurred during email summarization: {e}")
        send_telegram_message("❌ An error occurred while processing emails.")
        return "Error during summarization", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
