from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os

app = Flask(__name__, template_folder="templates")  # Ensure Flask looks for HTML files
CORS(app)  # Allow frontend to communicate with backend

openai.api_key = os.getenv("OPENAI_API_KEY")  # API Key from environment variables

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Serve the chatbot UI

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render requires explicit port setting
