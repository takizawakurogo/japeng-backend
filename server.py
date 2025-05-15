from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# 👉 Load .env locally; in Render your env vars are injected automatically
load_dotenv()

app = Flask(__name__)

# ✅ Read your key from the OPENAI_API_KEY env var
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    user_input = data.get("text", "")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful Japanese-English translator and grammar checker."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
