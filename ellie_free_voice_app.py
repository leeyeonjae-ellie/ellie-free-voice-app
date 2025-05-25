from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template, request, jsonify
import openai
from ellie_tts import speak

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_history = [
    {"role": "system", "content": "You are Ellie, a friendly English-speaking assistant. Respond naturally and helpfully in Korean or English depending on the user's language."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    chat_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_history,
            max_tokens=150,
            temperature=0.9
        )
        assistant_reply = response.choices[0].message["content"].strip()
        chat_history.append({"role": "assistant", "content": assistant_reply})

        speak(assistant_reply)

        return jsonify({"reply": assistant_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
