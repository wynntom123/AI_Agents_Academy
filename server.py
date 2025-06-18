from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# This allows CORS only from your frontend Netlify domain
CORS(app, resources={r"/*": {"origins": "https://whyhi.netlify.app"}})

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        # Handle preflight request directly
        return '', 200

    data = request.get_json()
    user_input = data.get("message")

    # Replace this with your OpenAI API call logic
    response = f"You said: {user_input}"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI chatbot that provides clear and concise answers."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/weather", methods=["POST"])
def get_weather():
    city = request.json.get("city", "")
    api_key = "your_weather_api_key"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()
        return jsonify({"weather": data["current"]["condition"]["text"], "temperature": data["current"]["temp_c"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

conversation_history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    conversation_history.append({"role": "user", "content": user_message})

    if len(conversation_history) > 5:  # Limit memory to last 5 messages
        conversation_history.pop(0)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI chatbot."}] + conversation_history
        )
        bot_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": bot_message})

        return jsonify({"response": bot_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
app.post("/wiki", async (req, res) => {
    const query = req.body.query;
    try {
        const response = await axios.get(`https://en.wikipedia.org/api/rest_v1/page/summary/${query}`);
        res.json({ summary: response.data.extract });
    } catch (error) {
        res.status(500).json({ error: "Unable to fetch data." });
    }
});