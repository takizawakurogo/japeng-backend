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
        response = openai.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a Japanese-English translator and grammar checker."},
                {"role": "user",   "content": user_input}
            ]
        )
        content = response.choices[0].message.content.strip()
        return jsonify({ "reply": content })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/health")
def health():
    return "OK", 200
