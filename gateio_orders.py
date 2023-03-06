import api

from configurations import setup_logger, basic_parameters

from gate_api import ApiClient, Configuration, FuturesApi, FuturesOrder, FuturesPriceTriggeredOrder, BatchFuturesOrder
from gate_api.exceptions import GateApiException

logger = setup_logger('gateio_orders')

ticker = basic_parameters['gateio_ticker']
settle = 'btc'


def try_to_send_order(initial, trigger):
    logger.info(trigger)
    price_triggered_order = FuturesPriceTriggeredOrder(
        initial = initial,
        trigger = trigger,
        order_type = 'close-long-position')
    try:
        resp = futures_api.create_price_triggered_order(settle, price_triggered_order)
        logger.info(resp) # ID
    except GateApiException as ex:
        logger.error("error encountered creating futures order: %s", ex)


def tpsl(order_response):
    filled_price = float(order_response.fill_price)
    deviation = 0.01
    if order_response.size > 0: # positive number means LONG position
        initial = {'contract': ticker, 'size': 0, 'price': '0', 'tif': 'ioc', 'auto_size' : 'close_long', 'reduce_only': True}

        # take profit
        price = str(round(filled_price + (filled_price/100) * deviation, 1))
        trigger = {'strategy_type': 0, 'price_type': 0, 'price': price, 'rule': 1} 
        try_to_send_order(initial, trigger)

        # stop loss
        price = str(round(filled_price - (filled_price/100) * deviation, 1))
        trigger = {'strategy_type': 0, 'price_type': 0, 'price': price, 'rule': 2} 
        try_to_send_order(initial, trigger)




# Initialize API client
# Setting host is optional. It defaults to https://api.gateio.ws/api/v4
config = Configuration(key=api.gateio_api_key, secret=api.gateio_api_secret)
futures_api = FuturesApi(ApiClient(config))
                            
# order using market price

order = FuturesOrder(contract=ticker, size=1, price='0', tif='ioc') # negative size to SHORT
try:
    order_response = futures_api.create_futures_order(settle, order)
    logger.info(order_response)
    tpsl(order_response)
except GateApiException as ex:
    logger.error("error encountered creating futures order: %s", ex)


''' OK
initial = {'contract': ticker, 'size': -1, 'price': '25000'}
trigger = {'strategy_type': 0, 'price_type': 0, 'price': '26000', 'rule': 1}
price_triggered_order = FuturesPriceTriggeredOrder(
    initial = initial,
    trigger = trigger,
    #order_type = 'close-long-order'
    )

try:
    resp = futures_api.create_price_triggered_order(settle, price_triggered_order)
    logger.info(resp)
except GateApiException as ex:
    logger.error("error encountered creating futures order: %s", ex)



initial = {'contract': ticker, 'size': 1, 'price': '21000'}
trigger = {'strategy_type': 0, 'price_type': 0, 'price': '20000', 'rule': 2}
price_triggered_order = FuturesPriceTriggeredOrder(
    initial = initial,
    trigger = trigger,
    #order_type = 'close-long-order'
    )

try:
    resp = futures_api.create_price_triggered_order(settle, price_triggered_order)
    logger.info(resp)
except GateApiException as ex:
    logger.error("error encountered creating futures order: %s", ex)
'''




''' OK
order = FuturesOrder(contract=ticker, size=1, price='0', tif='ioc') # negative size to SHORT

batch = [order]


try:
    resp = futures_api.create_batch_futures_order(settle, batch)
    logger.info(resp)
except GateApiException as ex:
    logger.error("error encountered creating futures order: %s", ex)

'''







''' examples
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