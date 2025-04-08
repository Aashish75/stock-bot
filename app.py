from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "3781ce7ccb0b418bb30ccf6f1313facf"  # Replace with your actual key

@app.route('/stock', methods=['POST'])
def stock_webhook():
    user_text = request.json.get('input', {}).get('text', '').lower()

    # Naive mapping from company name to stock symbol
    if 'apple' in user_text:
        symbol = 'AAPL'
    elif 'tesla' in user_text:
        symbol = 'TSLA'
    elif 'amazon' in user_text:
        symbol = 'AMZN'
    else:
        symbol = 'GOOGL'  # Default

    # Call Twelve Data API
    url = f'https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url).json()

    if 'price' in response:
        reply = f"The current price of {response['name']} ({symbol}) is ${response['price']}."
    else:
        reply = "Sorry, I couldn't fetch the stock info right now."

    return jsonify({
        "output": {
            "generic": [
                {
                    "response_type": "text",
                    "text": reply
                }
            ]
        }
    })

@app.route('/')
def index():
    return "Stock Bot is running!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

