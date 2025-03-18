from flask import Flask, request, jsonify
import openai
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows frontend to communicate with backend

# Set OpenAI API Key (Replace with your actual key)
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# CoinGecko API URL for real-time crypto data
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# AI Chatbot Endpoint
@app.route("/chat", methods=["POST"])
def chat():
user_message = request.json.get("message", "")

if not user_message:
return jsonify({"error": "No message provided"}), 400

# OpenAI GPT-4 API request
try:
response = openai.ChatCompletion.create(
model="gpt-4",
messages=[
{"role": "system", "content": "You are an AI crypto expert with an alien theme."},
{"role": "user", "content": user_message}
]
)
ai_reply = response["choices"][0]["message"]["content"]
return jsonify({"response": ai_reply})
except Exception as e:
return jsonify({"error": str(e)}), 500

# Crypto Market Data Endpoint
@app.route("/crypto-price", methods=["GET"])
def crypto_price():
coin = request.args.get("coin", "bitcoin").lower()
params = {"ids": coin, "vs_currencies": "usd"}
response = requests.get(COINGECKO_API_URL, params=params)

if response.status_code == 200:
return jsonify(response.json())
else:
return jsonify({"error": "Failed to fetch crypto data"}), 500

# Run the Flask app
if __name__ == "__main__":
app.run(debug=True)