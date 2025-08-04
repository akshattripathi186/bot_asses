from flask import Flask, request, jsonify
from db import init_db, fetch_user_profile, upsert_user_profile, fetch_recent_memory, store_chat_memory
from utils import detect_tone, extract_user_facts, build_gemini_prompt, fake_embedding, search_semantic_memory
from gemini_client import get_model, chat_with_gemini
from flask_cors import CORS

BOT_NAME = "Miko"
app = Flask(__name__)
CORS(app)
init_db()

@app.route("/", methods=["GET"])
def index():
    return "Miko Chatbot running! POST to /chat with user_id and message."

@app.route("/chat", methods=["POST"])
def api_chat():
    data = request.json
    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Provide user_id and message"}), 400

    user_id = str(data["user_id"])
    msg = data["message"]
    user_profile = fetch_user_profile(user_id)
    new_facts = extract_user_facts(msg)
    if new_facts:
        upsert_user_profile(user_id, new_facts)
        user_profile.update(new_facts)
    recent_msgs, mem_summaries = fetch_recent_memory(user_id)
    search_summary = search_semantic_memory(user_id, msg)
    tone = detect_tone(msg)
    prompt = build_gemini_prompt(user_id, msg, user_profile, recent_msgs, mem_summaries, search_summary, tone)

    model_instance = get_model()
    try:
        reply = chat_with_gemini(model_instance, prompt)
    except Exception as e:
        return jsonify({"error": "Gemini API error", "detail": str(e)}), 500

    # Store to memory
    words = msg[:120]
    memory_json = {
        "summary": f'User said: "{words}"',
        "embedding": fake_embedding(msg)
    }
    store_chat_memory(user_id, msg, memory_json)
    store_chat_memory(user_id, reply, {"summary": f"{BOT_NAME} said: {reply}", "embedding": fake_embedding(reply)})

    return jsonify({
        "bot": BOT_NAME,
        "reply": reply,
        "user_profile": user_profile
    })

@app.route("/profile/<user_id>")
def get_profile(user_id):
    return jsonify(fetch_user_profile(user_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
