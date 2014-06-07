import unittest
from test_utils import clear_redis_keys, init_db
from app.dbase.models import User, Order, Transaction
from app.market.utils import get_random_order
from app import db

class DatabaseRelationsTest(unittest.TestCase):

	"""
	Tests for the database. 
	"""	
	@init_db
	# @clear_redis_keys
	def setUp(self):
		pass
		
		# print 'Create books and orders etc.'
		# self.book = Orderbook()
		
	# def tearDown(self):
	# 	db.session.remove()
	# 	print 'Tear Down!'
	# 	db.drop_all()
	# 	print 'Tear down complete!'

	def test_db_initialization(self):
		self.assertTrue(len(User.query.all()) == 0)
		self.assertTrue(len(Order.query.all()) == 0)
		self.assertTrue(len(Transaction.query.all()) == 0)
	
	def test_database_insertion(self):
		self.assertTrue(len(User.query.all()) == 0)
		user = User.create(name = 'Halfdan')
		self.assertTrue(len(User.query.all()) == 1)

	def test_user_order_relations(self):
		user = User.create(name = 'Halfdan')
		order = Order.create(owner = user)
		retreived_user = User.query.filter_by(name = 'Halfdan').first()
		self.assertTrue(order.owner.id == retreived_user.id)

	def test_user_order_transaction_relatons(self):
		halfdan = User.create(name = 'Halfdan')
		sachie = User.create(name = 'Sachie')
		buy_order = Order.create(owner = halfdan, side = Order.BUY)
		sell_order = Order.create(owner = sachie, side = Order.SELL)
		transaction = Transaction(buy_order, sell_order, 1)
		
		halfdan_fromdb = User.query.filter_by(name = 'Halfdan').first()
		sachie_fromdb = User.query.filter_by(name = 'Sachie').first()
		
		self.assertTrue(transaction.buyer.id == halfdan_fromdb.id)
		self.assertTrue(transaction.seller.id == sachie_fromdb.id)