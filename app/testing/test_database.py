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
		user = User.create(nickname = 'Halfdan')
		self.assertTrue(len(User.query.all()) == 1)

	def test_user_order_relations(self):
		user = User.create(nickname = 'Halfdan')
		order = Order.create(owner = user)
		retreived_user = User.query.filter_by(nickname = 'Halfdan').first()
		self.assertTrue(order.owner.id == retreived_user.id)

	def test_user_order_transaction_relatons(self):
		buyer = User.create(nickname = 'buyer')
		seller = User.create(nickname = 'seller')
		buy_order = Order.create(owner = buyer, side = Order.BUY)
		sell_order = Order.create(owner = seller, side = Order.SELL)
		transaction = Transaction(buy_order, sell_order, 1)
		
		buyer_fromdb = User.query.filter_by(nickname = 'buyer').first()
		seller_fromdb = User.query.filter_by(nickname = 'seller').first()
		
		self.assertTrue(transaction.buyer.id == buyer_fromdb.id)
		self.assertTrue(transaction.seller.id == seller_fromdb.id)