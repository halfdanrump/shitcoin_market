from datetime import datetime
from pprint import pprint
import functools
# class testDecorator(initFunc):
# 	def __init__(self, **kwargs):
# 		print 'In __init__ of decorator'
# 		self.initFunc = initFunc

# 	def __call__(self, attr):
# 		print 'In call of decorator'
# 		self.initFunc()

# @testDecorator

class BaseMessage():
	
	def __init__(self, *subclass_attributes, **kwargs):
		self._allowedAttributes = ['owner']
		self._allowedAttributes += list(subclass_attributes)
		self.__dict__.update(dict(map(lambda key: (key, kwargs.get(key, None)), self._allowedAttributes)))
		self.created = datetime.utcnow()

	def __repr__(self):
		return repr(self.__dict__)


from datetime import datetime

@functools.total_ordering
class Order(BaseMessage):

	BUY = 'buy'
	SELL = 'sell'
	LIMIT = 'limit'
	MARKET = 'market'

	ID = 0
	
	def __init__(self, **kwargs):
		self.ID += 1
		self.created_at = datetime.utcnow()
		self._allowedAttributes = ['price', 'initial_volume', 'type', 'side']
		BaseMessage.__init__(self, *self._allowedAttributes, **kwargs)
		self.current_volume = self.initial_volume

	def __eq__(self, other_order):
		return isinstance(self, other_order.__class__) and self.price == other_order.price

	def __gt__(self, other_order):
		return self.price > other_order.price

	def is_sell(self):
		if self.side == self.SELL: return True
		else: return False

	def is_buy(self):
		if self.side == self.BUY: return True
		else: return False

	def is_limit(self):
		if self.type == self.LIMIT: return True
		else: return False

	def is_market(self):
		if self.type == self.MARKET: return True
		else: return False 

	def is_cheaper(self, other_order):
		if self.price < other_order.price: return True

	def get_details(self):
		return '%s order for %s shares at price %s'%(self.side, self.current_volume, self.price)