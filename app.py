import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.validators import validate_order_input
from bot.orders import execute_order
from bot.exceptions import BinanceAPIError, ValidationError
from bot.logging_config import logger

app = Flask(__name__)

# Load credentials
load_dotenv(".env")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/order", methods=["POST"])
def api_order():
    data = request.json
    
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("API credentials missing during UI order attempt")
        return jsonify({"success": False, "error": "API credentials missing. Please set BINANCE_TESTNET_API_KEY in .env"}), 400
        
    try:
        params = validate_order_input(
            symbol=data.get("symbol"),
            side=data.get("side"),
            order_type=data.get("type"),
            quantity=data.get("quantity"),
            price=data.get("price") if data.get("price") else None,
            stop_price=data.get("stop_price") if data.get("stop_price") else None
        )
        
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
        response_data = execute_order(client, params)
        
        return jsonify({"success": True, "data": response_data})
        
    except ValidationError as e:
        logger.warning(f"UI Validation Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except BinanceAPIError as e:
        logger.error(f"UI API Error: {str(e)}")
        return jsonify({"success": False, "error": f"API Error: {str(e)}"}), 400
    except Exception as e:
        logger.exception("UI Unexpected error")
        return jsonify({"success": False, "error": "An unexpected error occurred. Check the console logs."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
