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


# Make decorator for catching exceptions and writing them to log

def error_handler(f, *args):
	logger = current_app.logger
	def run():
		try:
			f(*args)
		except Exception, e:
			logger.error('Error detected: %s'%e)
	return run

# class test():
# 	def __init(self):
# 		self.p = multiprocessing.Process



class Orderbook():
	
	ID = 0

	def __init__(self):
		self.ID += 1
		self.buy_orders = Queue.PriorityQueue()
		self.sell_orders = Queue.PriorityQueue()
		self.logger = logging.getLogger(__name__)
	
	def start_auction(self, app):
		
		if not hasattr(self, 'daemon'):
			self.daemon = multiprocessing.Process(name = 'auction_%s'%self.ID, target = self.queue_daemon, args = (app,))		
			self.daemon.start()
			self.logger.info('Starting auciton for orderbook %s'%self.ID)

	def queue_daemon(self, app, rv_ttl=500):
		while True:
			msg = app.redis.blpop(app.config['order_queue'])
			self.logger.info('Received order')
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
		while True:
			if new_order.current_volume == 0:
				break
			matching_order = self.get_matching_order(new_order)
			if matching_order == None:
				#error_handler(self.add_order)(new_order)
				try:
					self.add_order(new_order)
				except Exception, e:
					self.logger.exception('Could not add order')
				break
			else:
				self.execute_transaction(new_order, matching_order)
			

	import heapq

	def get_matching_order(self, new_order):
		matching_order = None
		if new_order.is_buy():
			try:
				if new_order.price > self.sell_orders[0].price:
					matching_order = heapq.heappop(self.sell_orders)
			except IndexError:
				self.logger.exception('PROBLEM')
		elif new_order.is_sell():
			pass
		return None

	#@error_handler
	def add_order(self, new_order):
		self.logger.error('Adding order')
		if new_order.is_limit():
			if new_order.is_buy():
				self.buy_orders.put((new_order.price, new_order))
			elif new_order.is_sell():
				self.sell_orders.put((new_order.price, new_order))
		else:
			self.logger.debug('Discarding market order')
		self.logger.error('Standing orders: %s, %s'%(self.buy_orders.qsize(), self.sell_orders.qsize()))


	def execute_transaction(self, new_order, matching_order):
		pass