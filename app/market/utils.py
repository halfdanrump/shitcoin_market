from messages import Order
from numpy import random, abs, round

def get_random_order(side = None):
	volume = round(abs(random.normal(100, 30)))
	price = round(abs(random.normal(100, 30)))
	if not side:
		if random.random() > 0.5:
			side = Order.BUY
		else:
			side = Order.SELL
	order = Order(**{'initial_volume':volume, 'price':price, 'type':Order.LIMIT, 'side':side})
	return order

def get_many_random_orders(n_buy, n_sell):
	buy_orders = [get_random_order(Order.BUY) for i in range(n_buy)]
	sell_orders = [get_random_order(Order.SELL) for i in range(n_sell)]
	return buy_orders, sell_orders