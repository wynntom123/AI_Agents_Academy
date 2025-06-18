from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Allow requests only from your Netlify frontend
CORS(app, resources={r"/*": {"origins": "https://whyhi.netlify.app"}})

load_dotenv()  # Load API key from .env file
client = OpenAI()  # Will automatically use OPENAI_API_KEY from environment

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
