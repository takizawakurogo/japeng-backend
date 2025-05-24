from flask import Flask, request, jsonify
import openai
import os
import json

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
        # Ask ChatGPT for JSON when doing JP→EN, otherwise plain text reply
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Japanese-English translator and grammar checker."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        content = response.choices[0].message.content.strip()

        # Try to parse JSON
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            # Not JSON — return as simple reply
            return jsonify({ "reply": content })

        # If it has honorific/formal/casual, return as-is
        if all(k in parsed for k in ("honorific", "formal", "casual")):
            return jsonify({
                "honorific": parsed["honorific"],
                "formal":    parsed["formal"],
                "casual":    parsed["casual"]
            })
        else:
            # Otherwise, just echo back the parsed object under "reply"
            return jsonify({ "reply": content })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/health")
def health():
    return "OK", 200
