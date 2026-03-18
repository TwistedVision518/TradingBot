import argparse
import os
import sys
import json
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.validators import validate_order_input
from bot.orders import execute_order
from bot.exceptions import BinanceAPIError, ValidationError
from bot.logging_config import logger

def parse_args():
    parser = argparse.ArgumentParser(
        description="Simplified Trading Bot for Binance Futures Testnet"
    )
    
    parser.add_argument(
        "--symbol", type=str, required=True,
        help="Trading pair symbol (e.g., BTCUSDT)"
    )
    parser.add_argument(
        "--side", type=str, required=True, choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", type=str, required=True, choices=["MARKET", "LIMIT", "STOP_MARKET", "market", "limit", "stop_market"],
        help="Order type: MARKET, LIMIT, or STOP_MARKET"
    )
    parser.add_argument(
        "--quantity", type=float, required=True,
        help="Quantity to trade"
    )
    parser.add_argument(
        "--price", type=float, required=False,
        help="Price (Required for LIMIT orders)"
    )
    parser.add_argument(
        "--stop-price", type=float, required=False,
        help="Stop price (Required for STOP_MARKET orders)"
    )
    parser.add_argument(
        "--env", type=str, required=False, default=".env",
        help="Path to .env file containing API_KEY and API_SECRET"
    )

    return parser.parse_args()

def print_summary(params: dict):
    print("\n" + "="*40)
    print("ORDER REQUEST SUMMARY")
    print("="*40)
    print(f"Symbol     : {params['symbol']}")
    print(f"Side       : {params['side']}")
    print(f"Type       : {params['order_type']}")
    print(f"Quantity   : {params['quantity']}")
    
    if params['price']:
        print(f"Price      : {params['price']}")
    if params['stop_price']:
        print(f"Stop Price : {params['stop_price']}")
    print("="*40)

def print_response(success: bool, data: dict = None, error: str = None):
    print("\n" + "="*40)
    print("ORDER RESPONSE DETAILS")
    print("="*40)
    
    if success and data:
        print("[SUCCESS] Order placed successfully!")
        print(f"Order ID     : {data.get('orderId')}")
        print(f"Status       : {data.get('status')}")
        print(f"Executed Qty : {data.get('executedQty')}")
        print(f"Avg Price    : {data.get('avgPrice')}")
    else:
        print("[FAILURE] Order placement failed!")
        print(f"Error Reason : {error}")
        
    print("="*40 + "\n")

def main():
    args = parse_args()
    
    # Load credentials
    load_dotenv(args.env)
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("API credentials not found. Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET.")
        print("[ERROR] Missing API credentials in environment or .env file.")
        sys.exit(1)

    try:
        # Validate Input
        params = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        
        # Display request summary
        print_summary(params)
        
        # Initialize Client
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
        
        # Execute Order
        logger.info("Initializing order placement from CLI")
        response_data = execute_order(client, params)
        
        # Display success
        logger.info(f"Order successful. OrderID: {response_data.get('orderId')}")
        print_response(success=True, data=response_data)
        
    except ValidationError as e:
        logger.warning(f"Validation Error: {str(e)}")
        print_response(success=False, error=str(e))
        sys.exit(1)
        
    except BinanceAPIError as e:
        logger.error(f"API Error [{e.status_code}]: {e.error_code} - {str(e)}")
        print_response(success=False, error=str(e))
        sys.exit(1)
        
    except Exception as e:
        logger.exception("Unexpected error occurred.")
        print_response(success=False, error="An unexpected error occurred. Check logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
