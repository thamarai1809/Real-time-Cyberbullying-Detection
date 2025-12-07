import smtplib
from email.mime.text import MIMEText

sender_email = "dhana172022@gmail.com"
app_password = "rcsplvlpbeauvmoc"
receiver_email = "thamaraithamu18@gmail.com"

msg = MIMEText("Test mail from Python SMTP")
msg["Subject"] = "SMTP Test"
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
        print("✅ Test email sent successfully!")
except Exception as e:
    print("❌ Error:", e)
