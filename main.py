from configurations import setup_logger, basic_parameters
from multiprocessing import Process
from gateio_orders import order
from shared_dicts import SharedArray, SharedDict
from user_stream import user_stream

import binance_book_ws
import gateio_book_ws
import numpy as np

sqd = basic_parameters['shared_queue_dimensions']
logger = setup_logger('main')

# start listen gateio book_ticker websocket
Process(target=gateio_book_ws.book_ticker_stream).start()

# start listen binance book_ticker websocket
Process(target=binance_book_ws.book_ticker_spot_stream).start()

# start listen gateio user's private websocket
Process(target=user_stream).start()

deviations_array = np.zeros(100, dtype=np.float64)
binance_bid_prices_array = np.zeros(100, dtype=np.float64)

while True:
    queue = np.frombuffer(SharedArray.ws_arr.get_obj()).reshape(sqd) # ws_arr and arr share the same memory
    # current binance bid > previous binance bid
    # current binance bid > current gateio ask
    # current gateio ask > 0
    if queue[1, 2] > queue[0, 2] and queue[1, 2] > queue[1, 4] and queue[1, 4] > 0: 
        curr_binance_bid = queue[1, 2]
        curr_gateio_ask = queue[1, 4]
        
        binance_bid_prices_array[:-1] = binance_bid_prices_array[1:]
        binance_bid_prices_array[-1] = curr_binance_bid


        current_deviation = (curr_binance_bid - curr_gateio_ask) * 100 / curr_binance_bid
        if current_deviation != deviations_array[-1]:
            deviations_array[:-1] = deviations_array[1:]
            deviations_array[-1] = current_deviation

            binance_bid_prices_quantile05 = np.quantile(binance_bid_prices_array, 0.5) # 0.5 quantile of normal distribution
            if current_deviation >= 0.1 and SharedDict.orders['oco_filled'] and curr_binance_bid > binance_bid_prices_quantile05:
                SharedDict.orders['oco_filled'] = False
                logger.info('---------BUY----------')
                logger.info(f'current_deviation: {current_deviation} | curr_binance_bid {curr_binance_bid} | binance_bid_prices_quantile05 {binance_bid_prices_quantile05}')
                logger.info(queue)
                Process(target=order).start()

            #logger.info(deviations_array)
            #logger.info(f'current_deviation: {deviations_array[-1]}')
            #logger.info(queue)
            '''
            if deviations_array[0] > 0:
                quantile05 = np.quantile(deviations_array, 0.5) # 0.5 quantile of normal distribution
                logger.info(f'0.5 quantile of normal distribution: {quantile05} | current_deviation: {deviations_array[-1]}')
                if (current_deviation - quantile05) >= 0.01 and SharedDict.orders['oco_filled']:
                    SharedDict.orders['oco_filled'] = False
                    logger.info('---------BUY----------')
                    Process(target=order).start()
            '''

    #else:
    #    time.sleep(1)