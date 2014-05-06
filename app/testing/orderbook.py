import unittest
from test_utils import clear_redis_keys

from app.market.orderbook import Orderbook

class BasicOrderbookTests(unittest.TestCase):
	
	@clear_redis_keys
	def setUp(self):
		print 'Create books and orders etc...'
		self.book = Orderbook()

	def test(self):
		print 'RUNNING TEST'