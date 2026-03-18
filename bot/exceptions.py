class BinanceAPIError(Exception):
    """Custom exception raised for Binance API errors (HTTP failures or API returned error codes)."""
    def __init__(self, message, status_code=None, error_code=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code

class ValidationError(Exception):
    """Exception raised for invalid user input before hitting the API."""
    pass
