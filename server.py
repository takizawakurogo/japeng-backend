# server.py (minimal proxy version)

from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/translate", methods=["POST"])
def translate():
    payload = request.get_json()
    user_input = payload.get("text", "")

    try:
        # Directly forward user_input (the whole prompt) to ChatGPT:
        response = openai.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=[
                {"role": "system", "content": "You are a Japanese-English translator and grammar checker."},
                {"role": "user",   "content": user_input}
            ]
        )
        content = response.choices[0].message.content.strip()
        # Simply return the raw content under “reply” (always JSON)
        return jsonify({ "reply": content })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/health")
def health():
    return "OK", 200
