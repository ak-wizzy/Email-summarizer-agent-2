import os

# Email configuration
EMAIL_USER = os.getenv("EMAIL_USER")  # Email username
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Email password or app-specific password
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.mail.yahoo.com")  # Default IMAP server for Yahoo
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))  # Use default IMAP SSL port (993) for secure connection

# SMTP configuration for sending emails
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.mail.yahoo.com")  # Default SMTP server for Yahoo
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # Default SMTP SSL port (465) for secure sending

# Model configuration for summarization
MODEL_NAME = os.getenv("MODEL_NAME", "philschmid/bart-large-cnn-samsum")  # Set default model for summarization
