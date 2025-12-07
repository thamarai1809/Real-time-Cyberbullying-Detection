

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import state
# -------------------- IN-APP ALERT (Console) --------------------
def send_in_app_alert(user_id, message, risk_score):
    print(f"[IN-APP ALERT] user={user_id} risk={risk_score:.2f} message={message}")


# -------------------- EMAIL ALERT --------------------
# def send_alert_email(user_id, message, risk_score):
#     sender_email = "dhana172022@gmail.com"
#     app_password = "rcsplvlpbeauvmoc"   # Gmail App Password

#     # ✅ Try to use dynamic organiser email
#     try:
#         # from app import current_organiser_email

#         # import importlib
#         # app_module = importlib.import_module("app")
#         # importlib.reload(app_module)  # refresh the module
#         # current_organiser_email = getattr(app_module, "current_organiser_email", None)
#         current_organiser_email = state.current_organiser_email

        
        
        
        
#         if current_organiser_email:
#             receiver_email = current_organiser_email
#             print(f"📩 Sending alert to organiser: {receiver_email}")
#         else:
#             receiver_email = "fallbackmail@gmail.com"
#             print("⚠️ No organiser email found — using fallback.")
#     except Exception as e:
#         print("⚠️ Failed to import organiser email, using fallback:", e)
#         receiver_email = "fallbackmail@gmail.com"

#     # Email content
#     subject = "🚨 Toxic Message Detected in Google Meet"
#     body = f"""
#     Hello Organiser,

#     A toxic message was detected in your ongoing Google Meet.

#     👤 User: {user_id}
#     💬 Message: {message}
#     ⚠️ Risk Score: {risk_score:.2f}

#     Please review this incident promptly.

#     Regards,
#     Cyberbullying Detection System
#     """

#     msg = MIMEMultipart()
#     msg["From"] = sender_email
#     msg["To"] = receiver_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))

#     # Send email
#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender_email, app_password)
#             server.send_message(msg)
#             print("✅ Email alert sent successfully to:", receiver_email)
#     except Exception as e:
#         print(f"❌ Failed to send email alert: {e}")


def send_alert_email(user_id, message, risk_score, username=None, msg_time=None):
    sender_email = "dhana172022@gmail.com"
    app_password = "rcsplvlpbeauvmoc"   # Gmail App Password

    # ✅ Try to use dynamic organiser email
    try:
        current_organiser_email = state.current_organiser_email
        if current_organiser_email:
            receiver_email = current_organiser_email
            print(f"📩 Sending alert to organiser: {receiver_email}")
        else:
            receiver_email = "fallbackmail@gmail.com"
            print("⚠️ No organiser email found — using fallback.")
    except Exception as e:
        print("⚠️ Failed to import organiser email, using fallback:", e)
        receiver_email = "fallbackmail@gmail.com"

    # 📩 Email content
    subject = "🚨 Toxic Message Detected in Google Meet"
    body = f"""
Hello Organiser,

A toxic message was detected in your ongoing Google Meet.

👤 User: {username or user_id}
🕒 Time: {msg_time or 'Unknown'}
💬 Message: {message}
⚠️ Risk Score: {risk_score:.2f}

Please review this incident promptly.

Regards,
Cyberbullying Detection System
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print("✅ Email alert sent successfully to:", receiver_email)
    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")





















































































# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import state

# def send_in_app_alert(user_id, message, risk_score):
#     print(f"[IN-APP ALERT] user={user_id} risk={risk_score:.2f} message={message}")

# def send_alert_email(user_id, message, risk_score):
#     sender_email = "dhana172022@gmail.com"
#     app_password = "rcsplvlpbeauvmoc"

#     try:
#         current_organiser_email = state.current_organiser_email
        
#         if current_organiser_email:
#             receiver_email = current_organiser_email
#             print(f"📩 Sending alert to organiser: {receiver_email}")
#         else:
#             receiver_email = "fallbackmail@gmail.com"
#             print("⚠️ No organiser email found — using fallback.")
        
#     except Exception:
#         receiver_email = "fallbackmail@gmail.com"
#         print("⚠️ Failed to import organiser email, using fallback")

#     subject = "🚨 Toxic Message Detected in Google Meet"
#     body = f"""
# Hello Organiser,

# A toxic message was detected in your ongoing Google Meet.

# 👤 User: {user_id}
# 💬 Message: {message}
# ⚠️ Risk Score: {risk_score:.2f}

# Please review this incident promptly.

# Regards,
# Cyberbullying Detection System
# """

#     msg = MIMEMultipart()
#     msg["From"] = sender_email
#     msg["To"] = receiver_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender_email, app_password)
#             server.send_message(msg)
#             print("✅ Email alert sent successfully to:", receiver_email)
#     except Exception as e:
#         print(f"❌ Failed to send email alert: {e}")






# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import state

# # ---------------------------------------------------
# # 🔹 Email alert function
# # ---------------------------------------------------
# def send_alert_email(user_id, message, risk_score, username=None, time_sent=None):
#     organiser_email = getattr(state, "current_organiser_email", None)

#     if not organiser_email:
#         organiser_email = "fallbackmail@gmail.com"
#         print("⚠️ No organiser email found — using fallback.")

#     subject = "🚨 Toxic Message Detected in Meet"
#     body = f"""
# Hello Organiser,

# A toxic message was detected in your ongoing Google Meet.

# 👤 User: {username or user_id}
# 🕒 Time: {time_sent or 'Unknown'}
# 💬 Message: {message}
# ⚠️ Risk Score: {risk_score:.2f}

# Please review this incident promptly.

# Regards,
# Cyberbullying Detection System
# """

#     msg = MIMEMultipart()
#     msg["From"] = "noreply@cyberbullydetector.com"
#     msg["To"] = organiser_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))

#     try:
#         # --- SMTP server setup (example using Gmail) ---
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login("your_email@gmail.com", "your_app_password")
#             server.send_message(msg)
#         print("✅ Email alert successfully sent.")
#     except Exception as e:
#         print(f"❌ Failed to send email alert: {e}")


# # ---------------------------------------------------
# # 🔹 In-app banner notification
# # ---------------------------------------------------
# def send_in_app_alert(user_id, message, risk_score):
#     print(f"[IN-APP ALERT] user={user_id} risk={risk_score:.2f} message={message}")
