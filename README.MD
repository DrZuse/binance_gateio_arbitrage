# Trading Bot with Gate.io and Binance Websockets

This repository contains code snippets for a trading bot that utilizes websockets to monitor book tickers and execute orders on the Gate.io and Binance exchanges. The bot is written in Python and uses shared dictionaries and arrays for inter-process communication.

## Prerequisites

Before running the trading bot, make sure you have the following prerequisites installed:

- Python 3.x
- Gate.io API key and secret
- Binance API key and secret

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/trading-bot.git
   ```

2. Configure API keys:

   Open the `api.py` file and replace `gateio_api_key`, `gateio_api_secret`, `binance_api_key`, and `binance_api_secret` with your own API keys.

## Usage

1. Start listening to the Gate.io book ticker websocket:

   ```bash
   python gateio_book_ws.py
   ```

2. Start listening to the Binance book ticker websocket:

   ```bash
   python binance_book_ws.py
   ```

3. Start listening to the Gate.io user's private websocket:

   ```bash
   python user_stream.py
   ```

4. Run the main trading script:

   ```bash
   python main.py
   ```

   This script continuously monitors the book tickers from both exchanges and executes orders based on certain conditions.
