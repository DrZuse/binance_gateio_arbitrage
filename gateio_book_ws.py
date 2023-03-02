import asyncio

from gate_ws import Configuration, Connection, WebSocketResponse
from gate_ws.futures import FuturesBookTickerChannel
from configurations import basic_parameters, setup_logger

logger = setup_logger('gateio_book_ws')

ticker                  = basic_parameters['gateio_ticker']

# define your callback function on message received
def print_message(conn: Connection, response: WebSocketResponse):
    if response.error:
        print('error returned: ', response.error)
        conn.close()
        return
    print(response.result)


async def main():
    # initialize default connection, which connects to spot WebSocket V4
    # it is recommended to use one conn to initialize multiple channels
    conn = Connection(Configuration(app='futures', settle='btc'))

    # subscribe to any channel you are interested into, with the callback function
    channel = FuturesBookTickerChannel(conn, print_message)
    channel.subscribe(['BTC_USD'])

    # start the client
    await conn.run()


if __name__ == '__main__':
   #loop = asyncio.get_event_loop() # old versions of python
   loop = asyncio.new_event_loop()
   loop.run_until_complete(main())
   loop.close()