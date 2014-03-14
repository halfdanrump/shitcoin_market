import Queue
import logging


from flask import current_app
from pickle import loads, dumps

from uuid import uuid4

class DelayedResult(object):
    def __init__(self, key):
        self.key = key
        self._rv = None

    @property
    def return_value(self, orderbook):
        if self._rv is None:
            rv = current_app.redis.get(self.key)
            if rv is not None:
                self._rv = loads(rv)
        return self._rv


def queuefunc(f):
    def receive_order(*args, **kwargs):
    	print 'RECEIVING ORDER'
        qkey = current_app.config['order_queue']
        key = '%s:result:%s' % (qkey, str(uuid4()))
        print f
        s = dumps((f, key, args, kwargs))
        current_app.redis.rpush(current_app.config['order_queue'], s)
        return DelayedResult(key)
    f.receive_order = receive_order
    return f

@queuefunc
def test(order):
	print 'Adding an order...%s'%order

class Orderbook():
	
	#orderlog = logging.getLogger('orderlog')

	ID = 0

	def __init__(self):
		self.ID += 1

		# self.buy_orders = Queue.PriorityQueue()
		# self.sell_orders = Queue.PriorityQueue()
		
		# # Priority queue for storing orders until they can be processed (works as a buffer)
		# self.order_queue = Queue.PriorityQueue()


	# def add_order(self, order):
	# 	self.order_queue.put(order)


	@queuefunc		
	def process_order(self, order):
		print 'Adding order to orderbook!'
		# if order.is_limit():
		# 	if order.is_buy():
		# 		print order.get_details()
		# 		self.buy_orders.put()

		# 	elif order.side == order.SELL:
		# 		print order.get_details()
		# 	else:
		# 		raise Exception('Order side was not specified')
		# elif order.type == 'MARKET':
		# 	pass
		# else:
		# 	raise Exception('Order type was not specified')
		
		

		# return {'best_buy':0, 'best_sell':0}
		

# MRMAKRMJRE7M7