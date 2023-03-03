
import api
import asyncio


from gate_ws import Configuration, Connection, WebSocketResponse
from gate_ws.futures import FuturesOrderChannel, FuturesUserTradesChannel, FuturesPositionClosesChannel, FuturesPositionsChannel, FuturesAutoOrdersChannel
from gate_ws.spot import SpotOrderChannel
from configurations import basic_parameters, setup_logger

logger = setup_logger('user_stream')
ticker                       = basic_parameters['gateio_ticker']



async def main():
    #conn = Connection(Configuration(api_key=api.gateio_api_key, api_secret=api.gateio_api_secret))
    conn = Connection(Configuration(
        api_key = api.gateio_api_key,
        api_secret = api.gateio_api_secret,
        settle = 'btc',
        app = 'futures',
        
        ))

    channel = FuturesOrderChannel(conn, lambda c, r: print(r.result))
    channel.subscribe(['!all'])

    channel = FuturesUserTradesChannel(conn, lambda c, r: print(r.result))
    channel.subscribe(['!all'])

    channel = FuturesPositionClosesChannel(conn, lambda c, r: print(r.result))
    channel.subscribe(['!all'])

    channel = FuturesPositionsChannel(conn, lambda c, r: print(r.result))
    channel.subscribe(['!all'])

    channel = FuturesAutoOrdersChannel(conn, lambda c, r: print(r.result))
    channel.subscribe(['!all'])

    # start the client
    await conn.run()

if __name__ == '__main__':
    #loop = asyncio.get_event_loop() # old versions of python
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()

