from .exceptions import ValidationError

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_MARKET"]

def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """Validates user input before sending to the API."""
    
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string.")
        
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}.")
        
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}.")
        
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        raise ValidationError("Quantity must be a positive number.")
        
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price must be specified for LIMIT orders.")
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError("Price must be a positive number.")

    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValidationError("Stop price must be specified for STOP_MARKET orders.")
        try:
            stop_price = float(stop_price)
            if stop_price <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError("Stop price must be a positive number.")
            
    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
        "stop_price": stop_price
    }
