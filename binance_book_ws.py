import numpy as np
#import time

from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from configurations import basic_parameters, setup_logger
from shared_dicts import SharedArray


logger = setup_logger('binance_book_ws')

# =============================================================================
#   Basic parameters
# =============================================================================

ticker                      = basic_parameters['binance_ticker']
shared_queue_dimensions     = basic_parameters['shared_queue_dimensions'] # (2, 8)


# =======================================================================================
#   Connect to main LOB Websocket 
# =======================================================================================
#queue = np.zeros((2, 4), dtype=np.float32) # LOB |lowest ASK|lowest ASK size|highest BID|highest BID size|

def book_ticker_spot_stream():

    def message_handler(message):
        logger.info(message)
        if message.get('u') is None:
            return
            

        # in each new process create a new numpy array using:
        queue = np.frombuffer(SharedArray.ws_arr.get_obj()).reshape(shared_queue_dimensions) # ws_arr and arr share the same memory
        #global queue
        asks_bids = np.array([message['a'], message['A'], message['b'], message['B']], dtype=np.float64)

        queue[:-1, :4] = queue[1:, :4]
        queue[-1, :4] = asks_bids

        # in each new process create a new numpy array using:
        #arr = np.frombuffer(SharedArray.ws_arr.get_obj()).reshape(shared_queue_dimensions) # ws_arr and arr share the same memory


        # make it two-dimensional
        #b = arr.reshape(shared_queue_dimensions) # b and arr share the same memory
        
        #print(queue)
        #if asks_bids[4] == 1 and asks_bids[5] == 1 and SharedDict.orders['sell_order_status'] is None:
        #    logger.info('todo')




    my_client = Client()
    my_client.start()

    my_client.book_ticker(
        symbol = ticker,
        id = 2,
        callback = message_handler,
    )