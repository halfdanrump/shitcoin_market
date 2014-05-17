from app import db
from sqlalchemy.types import Enum
from uuid import uuid4
from copy import deepcopy
import json
import functools
from datetime import datetime


transaction_user_association = db.Table('transaction_user_association', db.metadata,
		db.Column( 'user_id', db.Integer, db.ForeignKey('users.id')),
		db.Column( 'transaction_id', db.Integer, db.ForeignKey('transactions.id'))
	)

transaction_order_association = db.Table('transaction_order_association', db.metadata,
		db.Column( 'order_id', db.Integer, db.ForeignKey('orders.id')),
		db.Column( 'transaction_id', db.Integer, db.ForeignKey('transactions.id'))
	)


class AutoCommit():
	def __init__(self, db_object):
		self.db_object = db_object
		print 'in decorator init'

	def __call__(self):
		instance = self.db_object()
		db.session.add(instance)
		db.session.commit()
		

@AutoCommit
class User(db.Model):
	"""
	Has bidirectional one-to-many relationship with Orders
	Has one-way relationship with Transactions
	"""
	__tablename__ = 'users'
	id = db.Column( db.Integer, primary_key = True )
	name = db.Column( db.String(100) )
	email = db.Column( db.String(100) )
	orders = db.relationship( 'Order', backref = 'owner', lazy = 'dynamic')
	transactions = db.relationship( 'Transaction', secondary = transaction_user_association, lazy = 'dynamic')

	
	def __init__(self):
		print 'in user init'

@AutoCommit
class Transaction(db.Model):
	__tablename__ = 'transactions'
	id = db.Column( db.Integer, primary_key = True )
	created_at = db.Column( db.DateTime )
	volume = db.Column( db.Integer )

	buy_order = db.relationship( 'Order', secondary = transaction_order_association, uselist = False, back_populates = 'transactions')
	sell_order = db.relationship( 'Order', secondary = transaction_order_association, uselist = False, back_populates = 'transactions')
	buyer = db.relationship( 'User', secondary = transaction_user_association, uselist = False, back_populates = 'transactions')
	seller = db.relationship( 'User', secondary = transaction_user_association, uselist = False, back_populates = 'transactions')
	

	
	
	def __init__(self, order1, order2, transaction_volume):
		self.created_at = datetime.utcnow()
		self.volume = transaction_volume
		self.order = order1
		if order1.is_buy() and order2.is_sell():
			self.buy_order = order1
			self.buyer = order1.owner
			self.sell_order = order2
			self.seller = order2.owner
		elif order1.is_sell() and order2.is_buy():
			self.buy_order = order2
			self.buyer = order2.owner
			self.sell_order = order1
			self.seller = order1.owner
		else:
			raise Exception


@AutoCommit
@functools.total_ordering
class Order(db.Model):
	__tablename__ = 'orders'
	BUY = 'buy'
	SELL = 'sell'
	LIMIT = 'limit'
	MARKET = 'market'

	_breeding_attributes = ['price', 'received', 'order_type', 'side', 'owner']

	id = db.Column( db.Integer, primary_key = True )
	
	created_at = db.Column ( db.DateTime )
	lag = received = db.Column ( db.Interval )
	price = db.Column( db.Integer )
	volume = db.Column( db.Integer )
	received = db.Column ( db.DateTime )
	order_type = db.Column( db.String(length = 6) )
	side = db.Column( db.String(length = 4) )
	
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	transactions = db.relationship( 'Transaction', secondary = transaction_order_association, lazy = 'dynamic')

	
	def __init__(self, **kwargs):
		self.uuid = uuid4().hex
		self.created_at = datetime.utcnow()
		# if kwargs.has_key('uuid'): self.uuid = kwargs['uuid'].hex
		if kwargs.has_key('price'): self.price = int(kwargs['price'])
		if kwargs.has_key('volume'): self.volume = int(kwargs['volume'])
		if kwargs.has_key('received'): 
			self.received = kwargs['received']
			self.lag = self.created_at - self.received
		if kwargs.has_key('order_type'): self.order_type = kwargs['order_type']
		if kwargs.has_key('side'): self.side = kwargs['side']
		if kwargs.has_key('owner'): self.owner = kwargs['owner']

	def __repr__(self):
		c = deepcopy(self.__dict__)
		if c.has_key('created_at'): c['created_at'] = c['created_at'].strftime('%Y-%m-%d-%H:%M')
		if c.has_key('received'): 
			c['received'] = c['received'].strftime('%Y-%m-%d-%H:%M')
			c['lag'] = c['lag'].total_seconds()
		try:
			c.pop('_sa_instance_state')
		except KeyError:
			pass
		return json.dumps(c)

	def breed(self, child_volume):
		
		child_dict = dict(map(lambda attr: (attr, getattr(self, attr)), self._breeding_attributes))
		child_dict.update({'volume': child_volume, 'uuid': uuid4().hex})
		return Order(**child_dict)

	def is_sell(self):
		if self.side == self.SELL: return True
		else: return False

	def is_buy(self):
		if self.side == self.BUY: return True
		else: return False

	def is_limit(self):
		if self.order_type == self.LIMIT: return True
		else: return False

	def is_market(self):
		if self.order_type == self.MARKET: return True
		else: return False 

	def __eq__(self, other_order):
		return isinstance(self, other_order.__class__) and self.price == other_order.price

	def __gt__(self, other_order):
		return self.price > other_order.price

























