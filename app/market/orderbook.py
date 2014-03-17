import Queue
import logging


from flask import current_app
from pickle import loads, dumps

from uuid import uuid4

import multiprocessing



class DelayedResult(object):
    def __init__(self, key):
        self.key = key
        self._rv = None

    @property
    def return_value(self):
        if self._rv is None:
            rv = current_app.redis.get(self.key)
            if rv is not None:
                self._rv = loads(rv)
        return self._rv


def queuefunc(f):
    def queue_order(order):
        qkey = current_app.config['order_queue']
        key = '%s:result:%s' % (qkey, str(uuid4()))
        s = dumps((key, order))
        print current_app.redis.rpush(current_app.config['order_queue'], s)
        return DelayedResult(key)
    f.queue_order = queue_order
    return f




class Orderbook():
	
	#orderlog = logging.getLogger('orderlog')

	ID = 0

	def __init__(self):
		self.ID += 1
		self.buy_orders = Queue.PriorityQueue()
		self.sell_orders = Queue.PriorityQueue()
		
	
	def start_auction(self, app):
		if not hasattr(self, 'daemon'):
			self.daemon = multiprocessing.Process(name = 'auction_%s'%self.ID, target = self.queue_daemon, args = (app,))		
			self.daemon.start()
		
	def queue_daemon(self, app, rv_ttl=500):
		print 'Starting auction daemon!'
		while True:
			print 'WAITING FOR ORDERS'
			msg = app.redis.blpop(app.config['order_queue'])
			print 'RECEIVED ORDERS'
			key, order = loads(msg[1])
			try:
				rv = self.process_order(order)
			except Exception, e:
				rv = e
			if rv is not None:
				app.redis.set(key, dumps(rv))
				app.redis.expire(key, rv_ttl)

	@queuefunc
	def process_order(self, new_order):
		matching_order = self.get_matching_order(new_order)
		print 'spank'
		#print 'Processing order %s'%order
		#return 'Processing complete message'

	

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
	def get_matching_order(self, new_order):
		return None