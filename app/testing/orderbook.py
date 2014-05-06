from tester import FocusDecorator, run_tests, active
from app.market.orderbook import Orderbook

from test_utils import MarketTester

@FocusDecorator
def test1():
        print 'Running test 1'

@FocusDecorator
def test2():
        print 'Running test 2'

# Use decorator too add functionality to 

# from test_utils import clear_redis_keys
# class TestInitDecorator():
# 	def __init__(self, test_class):
# 		self.setup = test_class.setUp
# 	def __call__(self):
		


import unittest
class OBTester(unittest.TestCase):
	def setUp():
		print 'Create books and orders etc...'

class OrderbookTests(MarketTester):

	def test_tets(self):
		print 'Running test test'