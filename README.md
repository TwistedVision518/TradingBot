# Binance Futures Testnet Trading Bot

Welcome! This is a simplified Python command-line application designed to execute **MARKET**, **LIMIT**, and **STOP_MARKET** orders on the Binance Futures Testnet.

It has been built from the ground up to be safe, reliable, and incredibly easy to use. It validates all inputs stringently before interacting with the network to protect you from making accidental invalid requests.

---

## 🎯 Features Checklist Complete
- ✅ **Places Market & Limit Orders** on Binance Futures Testnet (USDT-M)
- ✅ **Supports both sides**: BUY and SELL
- ✅ **Clean CLI validation**: Symbol, side, order type, quantity, and price.
- ✅ **Clear Terminal Output**: Summarizes the request before executing, and prints the exact order response details neatly.
- ✅ **Structured Code**: Cleanly separated folders for the `client`, `orders`, `validators`, and the main `cli.py`.
- ✅ **Proper Logging**: Records every single API request, response, and error transparently to `trading_bot.log`.
- ✅ **Exception Handling**: Gracefully catches user input errors, network failures, and Binance API rejections without crashing.
- ✅ **BONUS**: Implemented a third order type: `STOP_MARKET`.

---

## 🚀 How to Run the Bot (For Beginners!)

Don't worry if you aren't super technical! Follow these simple steps to get the bot running on your computer.

### Step 1: Install Python
You need Python installed on your computer. If you don't have it, download it from [Python's official website](https://www.python.org/downloads/) and install it.
> **Note for Windows users:** When installing, make sure to check the box that says "Add Python to PATH".

### Step 2: Get your Binance Testnet Keys
1. Go to the [Binance Futures Testnet](https://testnet.binancefuture.com/) and create a free account.
2. Once logged in, look for the **API Key** section (usually at the bottom of the dashboard or in the settings).
3. Generate a new API Key. You will be given an **API Key** and an **API Secret**. Keep these open in a tab, you'll need them in Step 4!

### Step 3: Install the Bot
Open your terminal (or Command Prompt / PowerShell on Windows) and navigate to this folder. Then, install the required libraries by running:
```bash
pip install -r requirements.txt
```

### Step 4: Add your API Keys
Create a new text file inside this folder and name it EXACTLY `.env` (don't forget the dot at the beginning!). 
Open the `.env` file in notepad and paste your keys like this:
```text
BINANCE_TESTNET_API_KEY=your_actual_api_key_here
BINANCE_TESTNET_API_SECRET=your_actual_api_secret_here
```
Save and close the file.

### Step 5: Place your first trade!
You're ready! Run the following commands in your terminal to tell the bot what to do.

**👉 To place a MARKET order (e.g. buying 0.01 BTC at the current market price):**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**👉 To place a LIMIT order (e.g. selling 0.05 BTC but only if the price hits $65,000):**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.05 --price 65000
```

**👉 To place a STOP MARKET order (e.g. selling 0.01 BTC if the price crashes to $60,000):**
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 60000
```

---

## 📂 Project Structure Explained
- `cli.py`: The main program you interact with over the terminal.
- `bot/client.py`: The communication layer. It talks directly to Binance and handles the complicated HMAC SHA256 security signatures automatically.
- `bot/validators.py`: The bodyguard. It checks your typing to make sure you didn't accidentally try to buy "-5" Bitcoin.
- `bot/orders.py`: The translation layer. Takes your validated CLI request and asks the client to execute it.
- `trading_bot.log`: The history book. You can open this file anytime to see a detailed, raw log of every single request made and exactly what Binance replied with!
- `.env`: (You create this). Holds your secret passwords so they don't get accidentally uploaded online.

## 📝 Assumptions Made
- The app uses Python's built-in `requests` library instead of an asynchronous framework like `httpx` or `aiohttp`. Since trading speed on a CLI-tool is restricted by human typing speed, `requests` is vastly simpler and much less prone to environment setup bugs.
- `TimeInForce` is hardcoded to `GTC` (Good Till Cancel) for LIMIT orders to avoid overwhelming the user with too many command-line arguments.
