import unittest
from test_utils import clear_redis_keys, init_db
from app.market.orderbook import Orderbook
from app.dbase.models import Order
from app.market.utils import get_random_order
from app import db

class BasicOrderbookTests(unittest.TestCase):
	"""
	Basic tests for adding and removing orders
	"""	
	@clear_redis_keys
	def setUp(self):
		# print
		# print 'Create books and orders etc.'
		self.book = Orderbook()

	def test_order_match_1(self):
		"""
		Matching orders with same price and same volume cancel out and are removed from the orderbook
		"""
		buy_order = get_random_order(price = 10, volume = 10, side = Order.BUY)
		self.book.process_order(buy_order)
		self.assertTrue(len(self.book.buy_orders) == 1)
		sell_order = get_random_order(price = 10, volume = 10, side = Order.SELL)
		self.book.process_order(sell_order)
		self.assertTrue(len(self.book.buy_orders) == 0)

	def test_order_match_2(self):
		"""
		Matching orders with same price but different volume result in a remaining order the subtracted volume
		"""
		buy_order = get_random_order(price = 10, volume = 5, side = Order.BUY)
		self.book.process_order(buy_order)
		self.assertTrue(len(self.book.buy_orders) == 1)
		sell_order = get_random_order(price = 10, volume = 10, side = Order.SELL)
		self.book.process_order(sell_order)
		self.assertTrue(len(self.book.buy_orders) == 0)
		self.assertTrue(len(self.book.sell_orders) == 1)
		remaining_order = self.book.sell_orders.pop()
		self.assertTrue(remaining_order.volume == 5)

	def test_order_match_3(self):
		"""
		Sell order eats two buy orders completely
		"""
		self.book.process_order(get_random_order(price = 10, volume = 5, side = Order.BUY))
		self.book.process_order(get_random_order(price = 11, volume = 5, side = Order.BUY))
		self.assertTrue(len(self.book.buy_orders) == 2)
		
		self.book.process_order(get_random_order(price = 10, volume = 10, side = Order.SELL))
		self.assertTrue(len(self.book.buy_orders) == 0)
		self.assertTrue(len(self.book.sell_orders) == 0)

	def test_order_match_4(self):
		"""
		Sell order eats cheapest buy order when cheapest buy order was added first
		"""
		self.book.process_order(get_random_order(price = 10, volume = 5, side = Order.BUY))
		self.book.process_order(get_random_order(price = 11, volume = 5, side = Order.BUY))
		self.assertTrue(len(self.book.buy_orders) == 2)

		self.book.process_order(get_random_order(price = 10, volume = 9, side = Order.SELL))
		self.assertTrue(len(self.book.buy_orders) == 1)
		self.assertTrue(len(self.book.sell_orders) == 0)
		
		remaining_order = self.book.buy_orders.pop()
		self.assertTrue(remaining_order.volume == 1)
		self.assertTrue(remaining_order.price == 11)
		
	def test_order_match_5(self):
		"""
		Sell order eats cheapest buy order when cheapest buy order was added last
		"""
		self.book.process_order(get_random_order(price = 11, volume = 5, side = Order.BUY))
		self.book.process_order(get_random_order(price = 10, volume = 5, side = Order.BUY))
		self.assertTrue(len(self.book.buy_orders) == 2)

		self.book.process_order(get_random_order(price = 10, volume = 9, side = Order.SELL))
		self.assertTrue(len(self.book.buy_orders) == 1)
		self.assertTrue(len(self.book.sell_orders) == 0)
		
		remaining_order = self.book.buy_orders.pop()
		self.assertTrue(remaining_order.volume == 1)
		self.assertTrue(remaining_order.price == 11)

	def test_order_match_6(self):
		"""
		Buy order eats cheapest sell order when cheapest sell order was added first
		"""
		self.book.process_order(get_random_order(price = 9, volume = 5, side = Order.SELL))
		self.book.process_order(get_random_order(price = 10, volume = 5, side = Order.SELL))
		self.assertTrue(len(self.book.sell_orders) == 2)

		self.book.process_order(get_random_order(price = 10, volume = 9, side = Order.BUY))
		self.assertTrue(len(self.book.buy_orders) == 0)
		self.assertTrue(len(self.book.sell_orders) == 1)
		
		remaining_order = self.book.sell_orders.pop()
		self.assertTrue(remaining_order.volume == 1)
		self.assertTrue(remaining_order.price == 10)

	def test_order_match_7(self):
		"""
		Buy order eats cheapest sell order when cheapest sell order was added last
		"""
		self.book.process_order(get_random_order(price = 10, volume = 5, side = Order.SELL))
		self.book.process_order(get_random_order(price = 9, volume = 5, side = Order.SELL))
		self.assertTrue(len(self.book.sell_orders) == 2)

		self.book.process_order(get_random_order(price = 10, volume = 9, side = Order.BUY))
		self.assertTrue(len(self.book.buy_orders) == 0)
		self.assertTrue(len(self.book.sell_orders) == 1)
		
		remaining_order = self.book.sell_orders.pop()
		self.assertTrue(remaining_order.volume == 1)
		self.assertTrue(remaining_order.price == 10)

