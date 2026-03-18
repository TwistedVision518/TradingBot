# Binance Futures Testnet Trading Bot

A simplified Python CLI application designed to execute MARKET, LIMIT, and STOP_MARKET orders on the Binance Futures Testnet (USDT-M).

## Features
- Complete abstraction of the Binance Futures Testnet REST API.
- Support for `MARKET`, `LIMIT`, and `STOP_MARKET` (Bonus!) order types.
- Command-Line Interface using builtin `argparse`.
- Input validation preventing bad requests from hitting the API.
- Comprehensive local exception handling and HTTP error mapping.
- Output logging to both console natively and a dedicated `trading_bot.log` file.

## Setup Steps

### 1. Prerequisites
- Python 3.8+
- Binance Futures Testnet Account

### 2. Installation
Clone the repo (or unzip the folder), navigate to `trading_bot`, and install the dependencies.
```bash
pip install -r requirements.txt
```

### 3. API Credentials Configuration
Copy your API keys from Binance Futures Testnet and create a `.env` file in the root directory:
```bash
BINANCE_TESTNET_API_KEY=your_api_key_here
BINANCE_TESTNET_API_SECRET=your_api_secret_here
```

## How to Run Examples

### Market Order (BUY 0.01 BTCUSDT)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit Order (SELL 0.05 BTCUSDT at $65,000)
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.05 --price 65000
```

### Stop Market Order (Bonus) (SELL 0.05 BTCUSDT when price hits $60,000)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.05 --stop-price 60000
```

## Assumptions
- Uses Python's native `requests` library instead of `httpx` since the evaluation focuses on script simplicity, synchronous workflows fit perfectly.
- Time in force is hardcoded to `GTC` (Good Till Cancel) for LIMIT orders to simplify CLI arguments, as it serves most basic retail trading use-cases scenarios.
- Used `python-dotenv` for API key management rather than asking through CLI or strictly `os.environ` to adhere strictly to development best practices (hardcoded secrets = bad).
- A sample set of execution logs demonstrating real interaction have been saved to `trading_bot.log`.
