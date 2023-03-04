import api

from configurations import setup_logger, basic_parameters
from decimal import Decimal as D, ROUND_UP, getcontext

from gate_api import ApiClient, Configuration, FuturesApi, FuturesOrder, Transfer, WalletApi, FuturesPriceTriggeredOrder
from gate_api.exceptions import GateApiException

logger = setup_logger('gateio_orders')

ticker = basic_parameters['gateio_ticker']
settle = 'btc'


def tpsl(order_response):
    #if order_response.get('size'):
    if order_response.result['size'] > 0: # LONG position
        initial = {'contract': ticker, 'size': -1, 'price': order_response['size'] + 1}
        trigger = {'strategy_type': 0, 'price_type': 0, 'price': order_response['size'] + 300, 'rule': 1}
        price_triggered_order = FuturesPriceTriggeredOrder(
            #contract = ticker,
            initial = initial,
            trigger = trigger,
            order_type = 'close-long-order'
            )
        
        try:
            resp = futures_api.create_price_triggered_order(settle, price_triggered_order)
            logger.info(resp)
        except GateApiException as ex:
            logger.error("error encountered creating futures order: %s", ex)



# Initialize API client
# Setting host is optional. It defaults to https://api.gateio.ws/api/v4
config = Configuration(key=api.gateio_api_key, secret=api.gateio_api_secret)
futures_api = FuturesApi(ApiClient(config))
                            
# order using market price
order = FuturesOrder(contract=ticker, size=1, price='0', tif='ioc') # negative size to SHORT
try:
    order_response = futures_api.create_futures_order(settle, order)
    logger.info(order_response)
    logger.info(type(order_response))
    #tpsl(order_response)
except GateApiException as ex:
    logger.error("error encountered creating futures order: %s", ex)
    


'''
########### simple order
url = '/futures/usdt/orders'
query_param = ''
body='{"contract":"BTC_USDT","size":6024,"iceberg":0,"price":"3765","tif":"gtc","text":"t-my-custom-id"}'
# for `gen_sign` implementation, refer to section `Authentication` above
sign_headers = gen_sign('POST', prefix + url, query_param, body)
headers.update(sign_headers)
r = requests.request('POST', host + prefix + url, headers=headers, data=body)
print(r.json())


########### batch
url = '/futures/usdt/batch_orders'
query_param = ''
body='[{"contract":"BTC_USDT","size":6024,"iceberg":0,"price":"3765","tif":"gtc","text":"t-my-custom-id"}]'
# for `gen_sign` implementation, refer to section `Authentication` above
sign_headers = gen_sign('POST', prefix + url, query_param, body)
headers.update(sign_headers)
r = requests.request('POST', host + prefix + url, headers=headers, data=body)
print(r.json())


########### price trigger
url = '/futures/usdt/price_orders'
query_param = ''
body='{"initial":{"contract":"BTC_USDT","size":100,"price":"5.03"},"trigger":{"strategy_type":0,"price_type":0,"price":"3000","rule":1,"expiration":86400},"order_type":"close-long-order"}'
# for `gen_sign` implementation, refer to section `Authentication` above
sign_headers = gen_sign('POST', prefix + url, query_param, body)
headers.update(sign_headers)
r = requests.request('POST', host + prefix + url, headers=headers, data=body)
print(r.json())
'''