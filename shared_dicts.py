from multiprocessing import Manager, Array

import ctypes as c
import numpy as np
import multiprocessing as mp

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


class SharedArray:
    # ws
    n, m = 2, 3
    ws_arr = mp.Array(c.c_double, n*m)
    

'''
https://stackoverflow.com/questions/9754034/can-i-create-a-shared-multiarray-or-lists-of-lists-object-in-python-for-multipro
n, m = 2, 3
mp_arr = mp.Array(c.c_double, n*m) # shared, can be used from multiple processes
# then in each new process create a new numpy array using:
arr = np.frombuffer(mp_arr.get_obj()) # mp_arr and arr share the same memory
# make it two-dimensional
b = arr.reshape((n,m)) # b and arr share the same memory
'''