
import api
import asyncio


from gate_ws import Configuration, Connection
from gate_ws.futures import FuturesOrderChannel
from configurations import basic_parameters, setup_logger
from shared_dicts import SharedDict

logger = setup_logger('user_stream')
ticker = basic_parameters['gateio_ticker']

def message_handler(r):
    print(r.result)
    #logger.info(f"result: {r.result[0]['reduce_only']}")
    if type(r.result) == 'list' and r.result[0]['is_reduce_only']: # TODO: change type detection with something more specific
        logger.info('set oco_filled to TRUE')
        SharedDict.orders['oco_filled'] = True


def user_stream(__name__ = '__main__'):
    logger.info('start listen users private stream')

    async def main():
        conn = Connection(Configuration(api_key=api.gateio_api_key, api_secret=api.gateio_api_secret, settle='btc', app='futures', test_net=False))

        channel = FuturesOrderChannel(conn, lambda c, r: message_handler(r))
        channel.subscribe([api.gateio_userid, ticker])

        # start the client
        await conn.run()


    if __name__ == '__main__':
        #loop = asyncio.get_event_loop() # old versions of python
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
        loop.close()



