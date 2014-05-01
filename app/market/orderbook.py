import Queue
import logging

from cPickle import loads

from uuid import uuid4

import multiprocessing
import heapq
from bisect import insort
### Logging setup


from app.market.messages import Order

from app import eventhandlers
from app import logger
from datetime import datetime
from redis import Redis
import time


class Orderbook():

	def __init__(self):
		self.ID = 'book_1' # + uuid4().hex
		self.buy_orders = list()
		self.sell_orders = list()
		self.redis = Redis()
		logger.info('ORDERBOOK INITIALIZED: %s'%self.ID)
		
		
	
	def start_auction(self):
		""" Run this to start the auction. If the auction is already running, nothing happens"""
		if not hasattr(self, 'daemon'):
			self.daemon = multiprocessing.Process(name = 'auction_%s'%self.ID, target = self.queue_daemon)		
			self.daemon.start()
			logger.info('Started auction for book %s'%self.ID)
		else:
			logger.info('Auction is already running at book %s'%self.ID)

	
	def stop_auction(self):
		if hasattr(self, 'daemon'):
			self.daemon.terminate()
			del self.daemon
			logger.info('Terminated auction at book %s'%self.ID)
		else:
			logger.info('Cannot stop auction that is not already running at book %s'%self.ID)

	
	def queue_daemon(self, rv_ttl=500):
		""" The daemon that listens for incoming orders. Must be run in a separate process. """
		while True:
			logger.debug('Waiting for orders...')
			order_form_data = self.redis.blpop(self.ID)
			order_form_data = loads(order_form_data[1])
			new_order = Order(**order_form_data)
			try:
				response = self.process_order(new_order)
				logger.debug('Finished processing order.')
			except Exception, e:
				logger.exception(e)
				response = e

	def process_order(self, new_order):
		logger.info('Processing order: %s'%new_order)
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
		logger.debug('Finished processing orders')
		eventhandlers.transmit_book_to_client(self)
		

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
		eventhandlers.transmit_transaction()

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
		for o in self.buy_orders: 
			buy_volume_dict[o.price] += o.current_volume
		sell_volume_dict = dict.fromkeys(set(self.get_sell_order_prices()), 0)
		for o in self.sell_orders: 
			sell_volume_dict[o.price] += o.current_volume
		return sorted(buy_volume_dict.items(), reverse = True), sorted(sell_volume_dict.items(), reverse = True)


if __name__ == "__main__":
	book = Orderbook()
	book.queue_daemon()
