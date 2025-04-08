from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "3781ce7ccb0b418bb30ccf6f1313facf"

# Simple company name to symbol mapping
COMPANY_SYMBOLS = {
    "apple": "AAPL",
    "tesla": "TSLA",
    "amazon": "AMZN",
    "microsoft": "MSFT",
    "google": "GOOGL"
}

@app.route('/stock', methods=['POST'])
def stock_webhook():
    user_text = request.json.get('text', '').lower()

    # Try to match company name in input
    symbol = None
    for company, sym in COMPANY_SYMBOLS.items():
        if company in user_text:
            symbol = sym
            break

    if not symbol:
        return jsonify({
            "output": {
                "generic": [{
                    "response_type": "text",
                    "text": "Sorry, I couldn't identify the company you're asking about."
                }]
            }
        })

    # Call Twelve Data API
    url = f'https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()

        if 'close' in data and 'name' in data:
            reply = f"The latest closing price of {data['name']} ({symbol}) was ${data['close']} on {data['datetime']}."
        else:
            reply = "Sorry, I couldn't fetch the stock info right now."
    except Exception as e:
        print("Error fetching data:", e)
        reply = "There was a problem fetching stock data."

    return jsonify({
        "output": {
            "generic": [{
                "response_type": "text",
                "text": reply
            }]
        }
    })

@app.route('/')
def index():
    return "Stock Bot is running!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
