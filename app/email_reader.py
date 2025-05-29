import imaplib
import email
from email.header import decode_header, make_header
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

def clean_sender(sender_field):
    """Extract a clean sender name/email from the From field."""
    if not sender_field:
        return "Unknown Sender"
    try:
        name, addr = email.utils.parseaddr(sender_field)
        return name if name else addr
    except Exception:
        return sender_field or "Unknown Sender"

def extract_body(msg):
    """Safely extract body from email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue

            try:
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break  # Prefer plain text if found
                elif content_type == "text/html" and not body:
                    html = part.get_payload(decode=True).decode(errors="ignore")
                    body = BeautifulSoup(html, "html.parser").get_text()
            except Exception:
                continue
    else:
        content_type = msg.get_content_type()
        try:
            if content_type == "text/plain":
                body = msg.get_payload(decode=True).decode(errors="ignore")
            elif content_type == "text/html":
                html = msg.get_payload(decode=True).decode(errors="ignore")
                body = BeautifulSoup(html, "html.parser").get_text()
        except Exception:
            body = ""
    return body.strip()

def fetch_unread_emails():
    """Fetch unread emails from the inbox."""
    imap_server = os.getenv("IMAP_SERVER")
    imap_user = os.getenv("IMAP_USER")
    imap_password = os.getenv("IMAP_PASSWORD")

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(imap_user, imap_password)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        print(f"Email IDs found: {email_ids}")

        if not email_ids:
            print("No unread emails found.")
            return []

        email_ids = [email_id.decode() for email_id in email_ids]
        print(f"Found {len(email_ids)} unread email(s). Fetching the last 15...")

        emails_to_fetch = email_ids[-15:] if len(email_ids) >= 15 else email_ids
        print(f"Fetching the following emails: {emails_to_fetch}")

        emails = []
        for email_id in emails_to_fetch:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject_raw = msg.get("Subject", "No Subject")
                    subject = str(make_header(decode_header(subject_raw)))

                    from_raw = msg.get("From", "Unknown Sender")
                    from_ = clean_sender(from_raw)

                    date = msg.get("Date", "Unknown Date")  # <-- New line to capture date
                    body = extract_body(msg)

                    emails.append({
                        "subject": subject,
                        "from": from_,
                        "date": date,          # <-- Included in dict
                        "body": body
                    })

        mail.logout()
        return emails
    except Exception as e:
        print(f"Error: {e}")
        return []
