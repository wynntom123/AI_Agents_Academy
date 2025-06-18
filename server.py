from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import requests
from dotenv import load_dotenv
import wikipedia

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
openai.api_key = openai_api_key

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://whyhi.netlify.app"}})

# In-memory conversation history (optional)
conversation_history = []

# Route for chatbot interaction
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 200  # Handle CORS preflight

    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Build conversation memory
    conversation_history.append({"role": "user", "content": user_message})
    if len(conversation_history) > 5:
        conversation_history.pop(0)

    # Build OpenAI prompt with weather and Wikipedia tools
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI chatbot that can fetch weather and Wikipedia info."}] + conversation_history
        )

        bot_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": bot_message})
        return jsonify({"response": bot_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for weather lookup
@app.route("/weather", methods=["POST"])
def get_weather():
    data = request.json
    city = data.get("city", "")
    api_key = os.getenv("WEATHER_API_KEY")  # Store your WeatherAPI key in .env

    if not city:
        return jsonify({"error": "City is required"}), 400

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()
        weather = data["current"]["condition"]["text"]
        temperature = data["current"]["temp_c"]
        return jsonify({"weather": weather, "temperature": temperature})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for Wikipedia lookup
@app.route("/wiki", methods=["POST"])
def get_wikipedia():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        summary = wikipedia.summary(query, sentences=2)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)