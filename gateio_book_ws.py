import asyncio
import numpy as np

from gate_ws import Configuration, Connection, WebSocketResponse
from gate_ws.futures import FuturesBookTickerChannel
from configurations import basic_parameters, setup_logger
from shared_dicts import SharedArray


logger = setup_logger('gateio_book_ws')

ticker                       = basic_parameters['gateio_ticker']
sqd                          = basic_parameters['shared_queue_dimensions']


def book_ticker_stream(__name__ = '__main__'):
    logger.info('start listen gateio book_ticker websocket')

    # define your callback function on message received
    def print_message(conn: Connection, response: WebSocketResponse):
        #logger.info(response.result)
        if response.error:
            logger.error('error returned: ', response.error)
            conn.close()
            return
        
        elif response.result.get('b'):
            # in each new process create a new numpy array using:
            queue = np.frombuffer(SharedArray.ws_arr.get_obj()).reshape(sqd) # ws_arr and arr share the same memory
            #global queue
            asks_bids = np.array([response.result['a'], response.result['A'], response.result['b'], response.result['B']], dtype=np.float64)

            queue[:-1, sqd[1]//2:] = queue[1:, sqd[1]//2:]
            queue[-1, sqd[1]//2:] = asks_bids
            


    async def main():
        # initialize default connection, which connects to spot WebSocket V4
        # it is recommended to use one conn to initialize multiple channels
        conn = Connection(Configuration(app='futures', settle='btc'))

        # subscribe to any channel you are interested into, with the callback function
        channel = FuturesBookTickerChannel(conn, print_message)
        channel.subscribe([ticker])

        # start the client
        await conn.run()


    if __name__ == '__main__':
        #loop = asyncio.get_event_loop() # old versions of python
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
        loop.close()