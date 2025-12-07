import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from preprocessing import preprocess_text
from toxicity import analyze_toxicity
from sentiment import analyze_sentiment
from decision import compute_risk_score, is_toxic
from database import log_message, fetch_flagged_messages
from alert import send_alert_email,send_in_app_alert
 #, send_alert_email  # ✅ Import both here
from config import RISK_THRESHOLD, DEV_MODE
import state
app = Flask(__name__)
CORS(app)

# current_organiser_email = None

@app.route("/")
def health():
    return "✅ Cyberbullying Detection Backend Running"


@app.route("/monitor", methods=["POST"])
def monitor():
    """
    Expects JSON:
    { "user_id": "...", "message": "...", "timestamp": "..." }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    user_id = data.get("user_id", "unknown")
    message = data.get("message", "")
    timestamp = data.get("timestamp", "")

    clean = preprocess_text(message)
    toxicity_score = analyze_toxicity(clean)
    sentiment_score = analyze_sentiment(clean)

    # You can extend this later (e.g., track user repetition)
    repetition_factor = 0.0

    risk_score = compute_risk_score(toxicity_score, sentiment_score, repetition_factor)
    flagged = is_toxic(risk_score)

    log_message(user_id, message, timestamp, risk_score)

    # if flagged:
    #     print("🚨 Toxic message detected — triggering alerts...")
    #     send_in_app_alert(user_id, message, risk_score)

    #     try:
    #         send_alert_email(user_id, message, risk_score)
    #         print("✅ Email alert successfully sent.")
    #     except Exception as e:
    #         print("❌ Email notification failed:", e)







    if flagged:
        print("🚨 Toxic message detected — triggering alerts...")
        send_in_app_alert(user_id, message, risk_score)

        # 🧩 Extract username, time, and message (if in 3-line format)
        username = ""
        msg_time = ""
        msg_text = message

        lines = [line.strip() for line in message.split("\n") if line.strip()]
        if len(lines) >= 3:
            username = lines[0]
            msg_time = lines[1]
            msg_text = "\n".join(lines[2:])
        elif len(lines) == 2:
            username = lines[0]
            msg_text = lines[1]
        else:
            msg_text = message

        try:
            send_alert_email(user_id, msg_text, risk_score, username=username, msg_time=msg_time)
            print("✅ Email alert successfully sent.")
        except Exception as e:
            print("❌ Email notification failed:", e)


    return jsonify({
        "status": "processed",
        "risk_score": risk_score,
        "flagged": bool(flagged),
        "user_id": user_id,
        "message": message
    }), 200


@app.route("/analyze", methods=["POST"])
def analyze():
    """Alias for /monitor – allows Chrome Extension to call /analyze."""
    return monitor()


@app.route("/get-flagged-messages", methods=["GET"])
def get_flagged():
    """Return messages with risk >= RISK_THRESHOLD (configurable)."""
    msgs = fetch_flagged_messages(limit=500, min_risk=RISK_THRESHOLD)
    return jsonify(msgs), 200
  # global memory

# @app.route("/update-organiser", methods=["POST"])
# def update_organiser():
#     global current_organiser_email
#     data = request.get_json()
#     # email = data.get("email")
#     email = data.get("email") or data.get("organiserEmail")  # match the frontend key

#     if email:
#         current_organiser_email = email
#         print(f"📧 Updated organiser email: {email}")
#         return jsonify({"status": "ok", "email": email})
#     return jsonify({"error": "no email provided"}), 400

@app.route("/update-organiser", methods=["POST"])
def update_organiser():
    # global current_organiser_email
    try:
        data = request.get_json(force=True)
        # your frontend might send "email" OR "organiserEmail" depending on implementation
        email = data.get("email") or data.get("organiserEmail")
        if not email:
            print("❌ No email found in request JSON:", data)
            return jsonify({"error": "no email provided"}), 400

        # current_organiser_email = email.strip()
        state.current_organiser_email = email.strip()
        print(f"📧 Updated organiser email: {state.current_organiser_email}")
        return jsonify({"status": "ok", "email": state.current_organiser_email}), 200

    except Exception as e:
        print("❌ Error updating organiser email:", e)
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # For development only
    app.run(host="127.0.0.1", port=5000, debug=False)





# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from preprocessing import preprocess_text
# from toxicity import analyze_toxicity
# from sentiment import analyze_sentiment
# from decision import compute_risk_score, is_toxic
# from database import log_message, fetch_flagged_messages
# from alert import send_alert_email, send_in_app_alert
# from config import RISK_THRESHOLD
# import state

# app = Flask(__name__)
# CORS(app)

# @app.route("/")
# def health():
#     return "✅ Cyberbullying Detection Backend Running"

# @app.route("/monitor", methods=["POST"])
# def monitor():
#     data = request.get_json(force=True, silent=True)
#     if not data:
#         return jsonify({"error": "invalid json"}), 400

#     user_id = data.get("user_id", "unknown")
#     message = data.get("message", "")
#     timestamp = data.get("timestamp", "")

#     clean = preprocess_text(message)
#     toxicity_score = analyze_toxicity(clean)
#     sentiment_score = analyze_sentiment(clean)
#     repetition_factor = 0.0

#     risk_score = compute_risk_score(toxicity_score, sentiment_score, repetition_factor)
#     flagged = is_toxic(risk_score)

#     log_message(user_id, message, timestamp, risk_score)

#     if flagged:
#         print(f"🚨 Toxic message detected — triggering alerts for user={user_id}")
#         send_in_app_alert(user_id, message, risk_score)
#         try:
#             send_alert_email(user_id, message, risk_score)
#         except Exception as e:
#             print("❌ Email notification failed:", e)

#     return jsonify({
#         "status": "processed",
#         "score": risk_score,
#         "flagged": bool(flagged),
#         "user_id": user_id,
#         "text": message
#     }), 200

# @app.route("/analyze", methods=["POST"])
# def analyze():
#     return monitor()

# @app.route("/update-organiser", methods=["POST"])
# def update_organiser():
#     try:
#         data = request.get_json(force=True)
#         email = data.get("email") or data.get("organiserEmail")
#         if not email:
#             return jsonify({"error": "no email provided"}), 400
#         state.current_organiser_email = email.strip()
#         print(f"📧 Updated organiser email: {state.current_organiser_email}")
#         return jsonify({"status": "ok", "email": state.current_organiser_email}), 200
#     except Exception as e:
#         print("❌ Error updating organiser email:", e)
#         return jsonify({"error": str(e)}), 500

# @app.route("/get-flagged-messages", methods=["GET"])
# def get_flagged():
#     msgs = fetch_flagged_messages(limit=500, min_risk=RISK_THRESHOLD)
#     return jsonify(msgs), 200

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=False)












# from flask import Flask, request, jsonify
# from alert import send_alert_email, send_in_app_alert
# import state

# app = Flask(__name__)

# # ---------------------------------------------------
# # 🔹 Update organiser email
# # ---------------------------------------------------
# @app.route("/update-organiser", methods=["POST"])
# def update_organiser():
#     try:
#         data = request.get_json(force=True)
#         email = data.get("email") or data.get("organiserEmail")

#         if not email:
#             print("❌ No email found in request JSON:", data)
#             return jsonify({"error": "no email provided"}), 400

#         state.current_organiser_email = email.strip()
#         print(f"📧 Updated organiser email: {state.current_organiser_email}")
#         return jsonify({"status": "ok", "email": state.current_organiser_email}), 200

#     except Exception as e:
#         print("❌ Error updating organiser email:", e)
#         return jsonify({"error": str(e)}), 500


# # ---------------------------------------------------
# # 🔹 Analyse / monitor route
# # ---------------------------------------------------
# @app.route("/analyze", methods=["POST"])
# def analyze_message():
#     data = request.get_json(force=True)
#     message = data.get("message", "")
#     user_id = data.get("user", "chrome-user")

#     # Simulated toxicity detection
#     risk_score = 0.61 if "ugly" in message or "kill" in message else 0.0
#     flagged = risk_score > 0.5

#     if flagged:
#         print("🚨 Toxic message detected — triggering alerts...")
#         send_in_app_alert(user_id, message, risk_score)

#         # 🧩 Extract username, time, and message lines
#         lines = [line.strip() for line in message.strip().splitlines() if line.strip()]
#         if len(lines) >= 3:
#             username = lines[0]
#             time_sent = lines[1]
#             actual_msg = "\n".join(lines[2:])
#         else:
#             username, time_sent, actual_msg = "Unknown", "Unknown", message

#         try:
#             send_alert_email(
#                 user_id,
#                 actual_msg,
#                 risk_score,
#                 username=username,
#                 time_sent=time_sent,
#             )
#             print("✅ Email alert successfully sent.")
#         except Exception as e:
#             print("❌ Email notification failed:", e)

#     return jsonify({"flagged": flagged, "risk_score": risk_score})


# if __name__ == "__main__":
#     app.run(debug=False)
