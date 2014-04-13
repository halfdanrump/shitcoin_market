import Queue
import logging


from flask import Flask, current_app
from pickle import loads, dumps

from uuid import uuid4

import multiprocessing
import heapq
from bisect import insort

### Logging setup

import logging.config, logging.handlers, yaml
config = yaml.load(open('app/config/log_conf.yaml'))
logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
handler = logging.handlers.RotatingFileHandler('app/logs/orderbook.log', maxBytes = 10**6)
#handler = logging.FileHandler('app/logs/orderbook.log')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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




# Make decorator for catching exceptions and writing them to log
import functools
def error_handler(f, *args, **kwargs):
	@functools.wraps(f) ### Necessary to update the module of the decorated function so that flask detects the right application context
	def run_safe(*args, **kwargs):
		try:
			f(*args, **kwargs)
		except Exception, e:
			logger.error('Error detected: %s'%e)
	return run_safe


"""
Make functions for processing orders pickeable so they can be pickled and stored in redis
"""


class Orderbook():

	def __init__(self):
		self.ID = uuid4()
		self.buy_orders = list()
		self.sell_orders = list()
		logger.info('ORDERBOOK INITIALIZED: %s'%self.ID)
		
	
	def start_auction(self, app):
		from threading import Thread
		""" Run this to start the auction. If the auction is already running, nothing happens"""
		if not hasattr(self, 'daemon'):
			# self.daemon = multiprocessing.Process(name = 'auction_%s'%self.ID, target = self.queue_daemon, args = (app,))		
			# self.daemon.start()
			self.daemon = Thread(target = self.queue_daemon, args = (app,))		
			self.daemon.start()
			logger.info('Started auciton for orderbook %s'%self.ID)



	def restart_auction(self, app):
		if hasattr(self, 'daemon'):
			self.daemon.terminate()
			del self.daemon
			logger.info('Terminated auction for orderbook %s'%self.ID)
			self.start_auction(app)
		else:
			logger.info('Cannot restart auction that is not already running at orderbook %s'%self.ID)

	
	def queue_order(self, order):
		logger.debug('Received order: %s'%order)
		qkey = current_app.config['order_queue']
		key = '%s:result:%s' % (qkey, str(uuid4()))
		s = dumps((key, order))
		current_app.redis.rpush(current_app.config['order_queue'], s)
		return DelayedResult(key)


	def queue_daemon(self, app, rv_ttl=500):
		""" The daemon that listens for incoming orders. Must be run in a separate process. """
		while True:
			print 'HAHAHAHA'
			msg = app.redis.blpop(app.config['order_queue'])
			key, order = loads(msg[1])
			try:
				response = self.process_order(order)
			except Exception, e:
				current_app.logger.exception(e)
				response = e
			if response is not None:
				app.redis.set(key, dumps(response))
				app.redis.expire(key, rv_ttl)

	#@error_handler
	def process_order(self, new_order):
		logger.debug('Processing order: %s'%new_order)
		while True:
			if new_order.current_volume == 0:
				logger.debug('Order volume depleted: %s'%new_order.ID)
				break

			matching_order = self.get_matching_order(new_order)
			
			logger.debug('Matching order: %s'%matching_order)
			if matching_order == None:
				self.add_order(new_order)
				break
			else:
				self.execute_transaction(new_order, matching_order)
				self.add_order(matching_order)
			logger.debug('Standing orders: %s, %s'%(len(self.buy_orders), len(self.sell_orders)))
		logger.debug('asdasdasdasdasd')
		
		logger.debug(self.get_cumulative_book())


	def get_matching_order(self, new_order):
		if new_order.is_buy() and self.has_sell_orders():				
			if new_order.price >= self.best_sell_price():
				return heapq.heappop(self.sell_orders)
		elif new_order.is_sell() and self.has_buy_orders():
			if new_order.price <= self.best_buy_price():
				return heapq.heappop(self.buy_orders)
		else:
			return None
		
	def add_order(self, new_order):
		if new_order.current_volume > 0:
			if new_order.is_limit():
				if new_order.is_buy():
					insort(self.buy_orders, new_order)
				elif new_order.is_sell():
					insort(self.sell_orders, new_order)
			else:
				logger.debug('Discarding market order')
		


	def execute_transaction(self, new_order, matching_order):
		transaction_volume = min(new_order.current_volume, matching_order.current_volume)
		new_order.current_volume -= transaction_volume
		matching_order.current_volume -= transaction_volume	

	def has_buy_orders(self):
		if len(self.buy_orders) > 0: return True
		else: return False

	def has_sell_orders(self):
		if len(self.sell_orders) > 0: return True
		else: return False

	def best_buy_price(self):
		try:
			return self.buy_orders[0].price
		except IndexError:
			return None

	def best_sell_price(self):
		try:
			return self.sell_orders[0].price
		except IndexError:
			return None

	def get_buy_order_prices(self):
		return [order.price for order in self.buy_orders]

	def get_sell_order_prices(self):
		return [order.price for order in self.sell_orders]

	def get_cumulative_book(self):
		buy_volume_dict = dict.fromkeys(set(self.get_buy_order_prices()), 0)
		for o in self.buy_orders: buy_volume_dict[o.price] += o.current_volume
		sell_volume_dict = dict.fromkeys(set(self.get_sell_order_prices()), 0)
		for o in self.sell_orders: sell_volume_dict[o.price] += o.current_volume
		return buy_volume_dict, sell_volume_dict



	