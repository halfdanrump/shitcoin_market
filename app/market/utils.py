from messages import Order
from datetime import datetime
import random

def get_random_order(side = None):
	volume = round(abs(random.gauss(100, 30)))
	price = round(abs(random.gauss(100, 30)))
	if not side:
		if random.random() > 0.5:
			side = Order.BUY
		else:
			side = Order.SELL
	received = datetime.utcnow()
	order = Order(**{'volume':volume, 'price':price, 'type':Order.LIMIT, 'side':side, 'received':received})
	return order

def get_random_order2(**kwargs):
	volume = round(abs(random.gauss(100, 30)))
	price = round(abs(random.gauss(100, 30)))
	if random.random() > 0.5:
		side = Order.BUY
	else:
		side = Order.SELL
	received = datetime.utcnow()
	order_args = {'volume':volume, 'price':price, 'type':Order.LIMIT, 'side':side, 'received':received}
	order_args = order_args.update(kwargs)
	order = Order(**order_args)
	return order


def get_many_random_orders(n_buy, n_sell):
	buy_orders = [get_random_order(Order.BUY) for i in range(n_buy)]
	sell_orders = [get_random_order(Order.SELL) for i in range(n_sell)]
	return buy_orders, sell_orders

def verify_order_data(order_data):
	try:
		int(order_data['price'])
		int(order_data['volume'])
	except ValueError:
		return False, 'Price and volume must be a number'
	except Exception, e:
		logger.exception(e)
	if order_data['type'] != Order.LIMIT and order_data['type'] != Order.MARKET:
		return False, 'Order type must be either LIMIT or MARKET'
	if order_data['side'] != Order.BUY and order_data['side'] != Order.SELL:
		return False, 'Order must be either BUY or SELL order'
	return True, 'Order validated successfully'



import functools
def error_handler(f, *args, **kwargs):
	@functools.wraps(f) ### Necessary to update the module of the decorated function so that flask detects the right application context
	def run_safe(*args, **kwargs):
		try:
			f(*args, **kwargs)
		except Exception, e:
			print e
			# logger.error('Error detected: %s'%e)
	return run_safe