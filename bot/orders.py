from .client import BinanceFuturesClient
from .logging_config import logger

def execute_order(client: BinanceFuturesClient, order_params: dict) -> dict:
    """
    Executes an order using the provided Binance client and validated parameters.
    Extracts the relevant information for the CLI output.
    """
    logger.info(f"Executing order via client for {order_params['symbol']}")
    
    response = client.place_order(
        symbol=order_params["symbol"],
        side=order_params["side"],
        order_type=order_params["order_type"],
        quantity=order_params["quantity"],
        price=order_params.get("price"),
        stop_price=order_params.get("stop_price")
    )
    
    # Extract only the useful parts for the CLI as per requirements
    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty", "0.0"),
        "avgPrice": response.get("avgPrice", "0.0"),
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type"),
    }
