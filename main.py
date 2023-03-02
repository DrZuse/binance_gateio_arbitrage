from configurations import setup_logger, basic_parameters
from multiprocessing import Process
from shared_dicts import SharedArray
import binance_book_ws
import gateio_book_ws
import numpy as np
import time

sqd = basic_parameters['shared_queue_dimensions']
logger = setup_logger('main')

# start listen binance book_ticker websocket
Process(target=binance_book_ws.book_ticker_spot_stream).start()


# start listen gateio book_ticker websocket
Process(target=gateio_book_ws.book_ticker_stream).start()


while True:
    queue = np.frombuffer(SharedArray.ws_arr.get_obj()).reshape(sqd) # ws_arr and arr share the same memory
    if queue[0, 0] > 0:
        logger.info(queue)
    else:
        time.sleep(1)