
from cPickle import loads

from threading import Thread
import heapq
from bisect import insort
from app.config.redis import RedisKeyManager



from app import eventhandlers
from app import logger
from redis import Redis
import time
import json
from app.utils import prefixed
from app.dbase.models import Order, Transaction
from app import db

class Market(object):
	def __init__(self, flapp):
		self.flapp = flapp
		flapp.market = self
		self.running_auctions = {}

	def start_auction(uuid):
		pass
		

class Orderbook(object):

	def __init__(self, uuid):
		self.uuid = uuid # + uuid4().hex
		self.keymanager = RedisKeyManager(uuid)				
		self.buy_orders = list()
		self.sell_orders = list()
		self.redis = Redis()
		logger.info('Initializing orderbook: %s'%self.uuid)
				
	
	def start_auction(self):
		""" Run this to start the auction. If the auction is already running, nothing happens"""
		if not hasattr(self, 'daemon'):
			self.daemon = Thread(name = 'auction_%s'%self.uuid, target = self.queue_daemon)		
			self.daemon.start()
			# self.osn = Thread(name = 'orderbookstatus_%s'%self.uuid, target = self.orderbook_status_notifier)		
			# self.osn.start()
			

			# Auction.query.filter_by(uuid = self.uuid).update({'running' : True})
			
			logger.info('Started auction for book %s'%self.uuid)
		else:
			logger.info('Auction is already running at book %s'%self.uuid)

	
	def stop_auction(self):
		if hasattr(self, 'daemon'):
			self.daemon.terminate()
			# Auction.query.filter_by(uuid = self.uuid).update({'running' : False})
			del self.daemon
			logger.info('Terminated auction at book %s'%self.uuid)
		else:
			logger.info('Cannot stop auction that is not already running at book %s'%self.uuid)

	
	def queue_daemon(self, rv_ttl=500):
		""" 
		The daemon that listens for incoming orders. Must be run in a separate process. 
		All received orders are stored in the database
		"""
		while True:
			logger.debug('Waiting for orders...')
			order_form_data = self.redis.blpop(prefixed(self.uuid))
			order_form_data = loads(order_form_data[1])
			new_order = Order(**order_form_data)
			self.store_order(new_order)
			try:
				response = self.process_order(new_order)
				logger.debug('Finished processing order.')
			except Exception, e:
				logger.exception(e)
				response = e

	def orderbook_status_notifier(self, rv_ttl = 400):
		while True:
			current_book = json.dumps(self.get_cumulative_book(as_json = True))
			logger.debug('Sent orderbook status to Redis: %s'%current_book)
			self.redis.set(self.keymanager['CUMULATIVE_BOOK'], json.dumps(self.get_cumulative_book(as_json = True)))
			time.sleep(1)

	def store_order(self, new_order):
		logger.debug('Committing order %s to database'%new_order)
		db.session.add(new_order)
		db.session.commit()

	def process_order(self, new_order):
		logger.info('Processing order: %s'%new_order)
		while True:
			if new_order.volume == 0:
				logger.debug('Order volume depleted: %s'%new_order.uuid)
				break

			matching_order = self.get_matching_order(new_order)
			
			logger.debug('Matching order: %s'%matching_order)
			if matching_order == None:
				self.add_order_to_auction(new_order)
				break
			else:
				new_order, child_matching = self.execute_transaction(new_order, matching_order)
				self.add_order_to_auction(child_matching)
			logger.debug('Standing orders: %s, %s'%(len(self.buy_orders), len(self.sell_orders)))
		logger.debug('Finished processing orders')

		self.redis.set(self.keymanager['CUMULATIVE_BOOK'], json.dumps(self.get_cumulative_book(as_json = True)))
		eventhandlers.transmit_book_to_client(self.keymanager['CUMULATIVE_BOOK'])
		

	def get_matching_order(self, new_order):
		if new_order.is_buy() and self.has_sell_orders():				
			if new_order.price >= self.best_sell_price():
				return heapq.heappop(self.sell_orders)
		elif new_order.is_sell() and self.has_buy_orders():
			if new_order.price <= self.best_buy_price():
				return heapq.heappop(self.buy_orders)
		else:
			return None
			
		
	def add_order_to_auction(self, new_order):
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
		
		transaction = Transaction(child_new, child_matching, transaction_volume)
		# transaction_volume.transmit_transaction(transaction.get_json())
		return child_new, child_matching


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





if __name__ == "__main__":
	book = Orderbook()
	book.queue_daemon()
