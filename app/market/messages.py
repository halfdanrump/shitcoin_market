from datetime import datetime
from pprint import pprint
import functools
from uuid import uuid4
import json


class BaseMessage():
	def __init__(self, *subclass_attributes, **kwargs):
		self._integerAttributes = ['price', 'volume']
		self._allowedAttributes = ['owner', 'received']
		self._allowedAttributes += list(subclass_attributes)
		self.__dict__.update(dict(map(lambda key: (key, kwargs.get(key, None)), self._allowedAttributes)))
		self.created_at = datetime.utcnow()
		print map(lambda attr: getattr(self, attr), self._integerAttributes)
		map(lambda attr: setattr(self, attr, int(getattr(self, attr))), self._integerAttributes)
		

	def __repr__(self):
		return repr(self.__dict__)

	def get_json(self):
		data = self.get_attributes()
		data['received'] = data['received'].strftime('%Y-%m-%d-%H:%M')
		return json.dumps(data)


class Transaction(BaseMessage):
	def __init__(self, order1, order2, db = None, **kwargs):
		assert isinstance(order1, Order) and isinstance(order2, Order), 'Transaction is initilaized by passing two order objects'
		self._allowedAttributes = ['buyer', 'seller', 'sell_order', 'buy_order', 'price', 'volume']
		BaseMessage.__init__(self, *self._allowedAttributes, **kwargs)
		




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
	
	def breed(self, child_volume):
		print self.get_attributes()
		child = Order(**self.get_attributes())
		# map(lambda attr: setattr(child, attr, getattr(self, attr)), self._allowedAttributes)
		child.volume = child_volume
		return child

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

	def get_attributes(self):
		return dict(map(lambda attr: (attr, getattr(self, attr)), self._allowedAttributes))

	def get_details(self):
		return '%s order for %s shares at price %s'%(self.side, self.volume, self.price)

	def __eq__(self, other_order):
		return isinstance(self, other_order.__class__) and self.price == other_order.price

	def __gt__(self, other_order):
		return self.price > other_order.price

	def __repr__(self):
		return str(dict(map(lambda x: (x, getattr(self, x)), self._allowedAttributes)))