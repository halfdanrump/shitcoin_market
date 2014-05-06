import Queue
import logging

from cPickle import loads

from uuid import uuid4

import multiprocessing
import heapq
from bisect import insort
### Logging setup


from app.market.messages import Order, Transaction

from app import eventhandlers
from app import logger
from datetime import datetime
from redis import Redis
import time
import json
from app.utils import prefixed

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
			order_form_data = self.redis.blpop(prefixed(self.ID))
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
			if new_order.volume == 0:
				logger.debug('Order volume depleted: %s'%new_order.ID)
				break

			matching_order = self.get_matching_order(new_order)
			
			logger.debug('Matching order: %s'%matching_order)
			if matching_order == None:
				self.add_order(new_order)
				break
			else:
				child_new, child_matching = self.execute_transaction(new_order, matching_order)
				new_order = child_new #This is sort of clumsy, but it will do for now.
				self.add_order(child_matching)
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
		if new_order.volume > 0:
			if new_order.is_limit():
				if new_order.is_buy():
					insort(self.buy_orders, new_order)
				elif new_order.is_sell():
					insort(self.sell_orders, new_order)
			else:
				logger.debug('Discarding market order')


	def execute_transaction(self, new_order, matching_order):
		transaction_volume = min( new_order.volume, matching_order.volume )
		child_new = new_order.breed( new_order.volume - transaction_volume )
		child_matching = matching_order.breed( matching_order.volume - transaction_volume )
		# transaction = Transaction()
		# eventhandlers.transmit_transaction(transaction.get_json())
		return child_new, child_matching

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

	def get_cumulative_book(self, as_json):
		assert isinstance(as_json, bool)
		buy_side = dict.fromkeys(set(self.get_buy_order_prices()), 0)
		for o in self.buy_orders: 
			buy_side[o.price] += o.volume
		sell_side = dict.fromkeys(set(self.get_sell_order_prices()), 0)
		for o in self.sell_orders: 
			sell_side[o.price] += o.volume

		buy_side = sorted(buy_side.items(), reverse = True)
		sell_side = sorted(sell_side.items(), reverse = True)

		if as_json:
			buy_side = json.dumps(buy_side)
			sell_side = json.dumps(sell_side)

		return buy_side, sell_side


if __name__ == "__main__":
	book = Orderbook()
	book.queue_daemon()
