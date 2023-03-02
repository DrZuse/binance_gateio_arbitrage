import numpy as np
#import time

from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from configurations import basic_parameters, setup_logger
from shared_dicts import SharedArray


logger = setup_logger('binance_book_ws')

# =============================================================================
#   Basic parameters
# =============================================================================

ticker                  = basic_parameters['binance_ticker']


# =======================================================================================
#   Connect to main LOB Websocket 
# =======================================================================================
queue = np.zeros((2, 6), dtype=np.float32) # LOB |lowest ASK|lowest ASK size|highest BID|highest BID size | spread% | grow (0|1) |

def book_ticker_spot_stream():

    def message_handler(message):
        print(message)
        if message.get('u') is None:
            return
            
        global queue
        asks_bids = np.array([message['a'], message['A'], message['b'], message['B'], 0, 0], dtype=np.float64)
        asks_bids[4] = np.where(((asks_bids[0] - asks_bids[2]) * 100 / asks_bids[2]) > 0.05, 1, 0) # spread% > 0.05% : true == 1 | false == 0
        asks_bids[5] = np.where(asks_bids[0] > queue[1][0], 1, 0) # grow : true == 1 | false == 0

        queue[:-1] = queue[1:]
        queue[-1] = asks_bids

        # in each new process create a new numpy array using:
        arr = np.frombuffer(SharedArray.ws_arr.get_obj()) # ws_arr and arr share the same memory

        
        # make it two-dimensional
        b = arr.reshape((n,m)) # b and arr share the same memory
        
        #print(queue)
        if asks_bids[4] == 1 and asks_bids[5] == 1 and SharedDict.orders['sell_order_status'] is None:
            logger.info('todo')




    my_client = Client()
    my_client.start()

    my_client.book_ticker(
        symbol = ticker,
        id = 2,
        callback = message_handler,
    )