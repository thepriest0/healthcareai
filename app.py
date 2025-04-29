from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the API key from environment
GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")
GITHUB_ENDPOINT = "https://models.github.ai/inference"
MODEL_NAME = "openai/gpt-4.1"

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '')

    try:
        response = requests.post(
            f"{GITHUB_ENDPOINT}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GITHUB_TOKEN}"
            },
            json={
                "messages": [
                    {"role": "system", "content": (
                        "You are HealthGuide AI, a professional virtual health assistant. "
                        "Only answer health-related questions about symptoms, diseases, treatments, medications, nutrition, mental health, and preventive care. "
                        "If the user asks a question outside health topics (e.g., politics, coding, history, entertainment, etc), politely respond: "
                        "'I'm sorry, I can only provide information about health and wellness topics.' "
                        "Always prioritize user safety. If the question is serious, advise users to consult a qualified healthcare provider. "
                        "Answer clearly and in a human-friendly way, using organized paragraphs, line breaks, and appropriate emojis where helpful to make the response engaging and easy to read."
                    )},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "top_p": 1.0,
                "model": MODEL_NAME
            }
        )

        if response.status_code != 200:
            return jsonify({'reply': "Sorry, something went wrong connecting to the server."}), 500

        reply = response.json()['choices'][0]['message']['content']
        return jsonify({'reply': reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({'reply': "Sorry, server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)
