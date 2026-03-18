import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

from .exceptions import BinanceAPIError
from .logging_config import logger

class BinanceFuturesClient:
    """Wrapper for Binance Futures Testnet REST API."""
    
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _generate_signature(self, params: dict) -> str:
        """Generates HMAC SHA256 signature for API requests."""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """Helper to send HTTP requests to Binance and handle errors."""
        url = f"{self.BASE_URL}{endpoint}"
        
        if params is None:
            params = {}
            
        # Add timestamp required by Binance signed endpoints
        params['timestamp'] = int(time.time() * 1000)
        
        params['signature'] = self._generate_signature(params)

        logger.debug(f"Sending {method} request to {url} with params: {params}")

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                # Binance prefers x-www-form-urlencoded for POST
                response = self.session.post(url, data=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response_json = response.json()
            
            # API returns error codes inside JSON sometimes
            if 'code' in response_json and 'msg' in response_json:
                if response_json['code'] < 0:
                    raise BinanceAPIError(
                        message=response_json['msg'],
                        status_code=response.status_code,
                        error_code=response_json['code']
                    )
            
            response.raise_for_status()
            logger.debug(f"Received response: {response_json}")
            return response_json
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during {method} {url}: {str(e)}")
            # If we got a response with error details from the server, parse it
            if hasattr(e, 'response') and e.response is not None:
                try:
                    err_data = e.response.json()
                    raise BinanceAPIError(
                        message=err_data.get('msg', str(e)),
                        status_code=e.response.status_code,
                        error_code=err_data.get('code')
                    )
                except ValueError:
                    pass
            raise BinanceAPIError(f"Network error: {str(e)}")

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None, time_in_force: str = "GTC") -> dict:
        """Places a new order."""
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }
        
        if order_type.upper() == "LIMIT":
            if not price:
                raise ValueError("Price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force
            
        if order_type.upper() == "STOP_MARKET":
            if not stop_price:
                raise ValueError("Stop price is required for STOP_MARKET orders.")
            params["stopPrice"] = stop_price

        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
        
        return self._request("POST", endpoint, params)
