import logging
import os

# =============================================================================
# Basic parameters
# =============================================================================
basic_parameters = dict()
basic_parameters['binance_ticker']                  = 'BTCUSDT'
basic_parameters['gateio_ticker']                   = 'BTC_USD'
basic_parameters['shared_queue_dimensions']         = (2,3)

# =============================================================================
# Logs
# =============================================================================

logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

formatter = logging.Formatter('\n\r[%(asctime)s.%(msecs)03d] %(levelname)s [%(filename)s.%(process)d.%(thread)d.%(funcName)s:%(lineno)d]\n\r%(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)

# To setup as many loggers as you want
# example: main_logger = setup_logger('main_logger')
def setup_logger(name, level=logging.DEBUG, logs_dir=logs_dir):
    
    log_file = logs_dir + '/' + name + '.log'

    handler = logging.FileHandler(log_file, mode='w')        
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console)

    return logger