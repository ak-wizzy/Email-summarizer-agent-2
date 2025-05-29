import smtplib, ssl, os

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465, context=context) as server:
    server.login("ma_rapgame@yahoo.com", "=mnheuebjjekmhhdg")
    print("✅ Logged in successfully")
