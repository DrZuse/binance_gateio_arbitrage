from multiprocessing import Manager

######################################################
# Создаем словари доступные из всех потоков
######################################################

class SharedDict:

    manager = Manager()

    # orders
    orders = manager.dict()
    orders['oco_filled'] = None
    orders['wait'] = 0
    orders['tp_counter'] = 0
    orders['sell_order_status'] = None # try_to_open | in_SHORT_position | try_to_revert | in_LONG_position
    orders['sell_order_timestamp'] = None