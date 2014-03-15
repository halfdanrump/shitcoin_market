from messages import Order
from numpy import random, abs, round

def get_random_order():
	volume = round(abs(random.normal(100, 30)))
	price = round(abs(random.normal(100, 30)))
	if random.random() > 0.5:
		side = Order.BUY
	else:
		side = Order.SELL
	order = Order(**{'initial_volume':volume, 'price':price, 'type':Order.LIMIT, 'side':side})
	return order
	
