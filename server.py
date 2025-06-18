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
weather_api_key = os.getenv("WEATHER_API_KEY")

# Initialize OpenAI
openai.api_key = openai_api_key

# Initialize Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://whyhi.netlify.app"}})

# Helper function for weather
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
    response = requests.get(url)
    data = response.json()
    condition = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]
    return f"The weather in {city} is {condition} with a temperature of {temperature}°C."

# Helper function for Wikipedia
def get_wikipedia_summary(topic):
    summary = wikipedia.summary(topic, sentences=2)
    return summary

# Main chat route
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 200

    data = request.json
    user_message = data.get("message", "").lower()

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Simple intent detection
    if "weather" in user_message:
        # Hard-coded city for now; ideally you'd extract this from user_message
        city = "Los Angeles"
        try:
            weather_info = get_weather(city)
            return jsonify({"response": weather_info})
        except Exception as e:
            return jsonify({"response": f"Error fetching weather: {str(e)}"})

    if "wikipedia" in user_message or "wiki" in user_message:
        # Hard-coded topic for now; ideally you'd extract this too
        topic = "Python (programming language)"
        try:
            summary = get_wikipedia_summary(topic)
            return jsonify({"response": summary})
        except Exception as e:
            return jsonify({"response": f"Error fetching Wikipedia summary: {str(e)}"})

    # Default behavior: use OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_message = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_message})
    except Exception as e:
        return jsonify({"response": f"Error calling OpenAI: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)