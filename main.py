from configurations import setup_logger
from multiprocessing import Process
from binance_book_ws import book_ticker_spot_stream

logger = setup_logger('main')

# start listen binance book_ticker websocket
Process(target=book_ticker_spot_stream).start()