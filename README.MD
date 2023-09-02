# Trading Bot with Gate.io and Binance Websockets

This repository contains code snippets for a trading bot that utilizes websockets to monitor book tickers and execute orders on the Gate.io and Binance exchanges. The bot is written in Python and makes use of multiprocessing, ctypes, numpy, and asyncio for efficient and inter-process communication.

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

   Create an `api.py` file and place `gateio_api_key`, `gateio_api_secret`, `binance_api_key`, and `binance_api_secret` with your own API keys.

## Usage

1. Run the main trading script:

   ```bash
   python main.py
   ```

   This script continuously monitors the book tickers from both exchanges and executes orders based on certain conditions.

## Explanation

1. Start listening to the Gate.io book ticker websocket:

   ```python
   Process(target=gateio_book_ws.book_ticker_stream).start()
   ```

   This script utilizes the `multiprocessing` module to run the websocket client in a separate process. It also uses `numpy` to store and manipulate the book ticker data efficiently.

2. Start listening to the Binance book ticker websocket:

   ```python
   Process(target=binance_book_ws.book_ticker_spot_stream).start()
   ```

   Similar to the Gate.io script, this script also utilizes `multiprocessing` and `numpy` for efficient processing of book ticker data.

3. Start listening to the Gate.io user's private websocket:

   ```python
   Process(target=user_stream).start()
   ```

   This script uses `asyncio` to run the websocket client asynchronously, allowing for concurrent processing of user stream data.


   The main script combines the book ticker data from both exchanges and executes orders based on certain conditions. It utilizes `multiprocessing` for running the book ticker websockets in separate processes, `ctypes` for shared memory communication between processes, and `numpy` for efficient data manipulation.