from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.chat.utils import call_chatgpt
from app.chat.prompts import SYSTEM_PROMPT
from app.chat.tools import TOOLS

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Napisz coś 🙂"})

    history = session.get("chat_history", [])

    history.append({"role": "user", "content": user_msg})

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history
    ]

    try:
        bot_reply = call_chatgpt(
            messages=messages,
            tools=TOOLS,
            user_id=current_user.id
        )
    except Exception as e:
        print("Chat error:", e)
        bot_reply = "Ups, coś poszło nie tak 😅"

    history.append({"role": "assistant", "content": bot_reply})
    session["chat_history"] = history[-20:]

    return jsonify({"reply": bot_reply})



@chat_bp.route("/api/chat/history")
def chat_history():
    return jsonify(session.get("chat_history", []))