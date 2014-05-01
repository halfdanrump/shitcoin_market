from datetime import datetime
from pprint import pprint
import functools
# from app import logger# eventhandlers
# from .. import eventhandlers
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
		self._integerAttributes = ['price', 'volume']
		try:
			self._allowedAttributes = ['owner', 'received']
			self._allowedAttributes += list(subclass_attributes)
			self.__dict__.update(dict(map(lambda key: (key, kwargs.get(key, None)), self._allowedAttributes)))
			self.created_at = datetime.utcnow()
			map(lambda a: setattr(self, attr, int(getattr(self, attr))), self._integerAttributes)
		except Exception, e:
			pass
			# logger.exception(e)
			#eventhandlers.invalid_message(e)
		
	def __repr__(self):
		return repr(self.__dict__)


class Transaction(BaseMessage):
	def __init__(self, **kwargs):
		self._allowedAttributes = ['buyer', 'seller', 'sell_order', 'buy_order', 'price', 'volume']
		BaseMessage.__init__(self, *self._allowedAttributes, **kwargs)


from datetime import datetime
from uuid import uuid4

@functools.total_ordering
class Order(BaseMessage):

	BUY = 'buy'
	SELL = 'sell'
	LIMIT = 'limit'
	MARKET = 'market'
	
	def __init__(self, **kwargs):
		self.ID = uuid4()
		self.created_at = datetime.utcnow()
		self._allowedAttributes = ['price', 'volume', 'type', 'side']
		BaseMessage.__init__(self, *self._allowedAttributes, **kwargs)


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
		return '%s order for %s shares at price %s'%(self.side, self.volume, self.price)

	def __eq__(self, other_order):
		return isinstance(self, other_order.__class__) and self.price == other_order.price

	def __gt__(self, other_order):
		return self.price > other_order.price

	def __repr__(self):
		return str(dict(map(lambda x: (x, getattr(self, x)), self._allowedAttributes)))