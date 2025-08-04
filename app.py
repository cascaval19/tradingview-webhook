from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Cheile Alpaca – vor fi setate în Render ca Environment Variables
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("Received data:", data)

    if data and 'ticker' in data and 'action' in data:
        symbol = data['ticker']
        side = data['action'].lower()

        order = {
            "symbol": symbol,
            "qty": 1,
            "side": side,
            "type": "market",
            "time_in_force": "gtc"
        }

        response = requests.post(
            f"{BASE_URL}/v2/orders",
            json=order,
            headers={
                "APCA-API-KEY-ID": ALPACA_API_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
            }
        )

        print("Alpaca response:", response.json())
        return jsonify({"status": "Order sent", "alpaca_response": response.json()})

    return jsonify({"error": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
