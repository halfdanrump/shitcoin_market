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
	
def queue_daemon(app, rv_ttl=500):
    from pickle import loads
    while True:
        msg = app.redis.blpop(app.config['order_queue'])
        func, key, args, kwargs = loads(msg[1])
        try:
            rv = func(*args, **kwargs)
        except Exception, e:
            rv = e
        if rv is not None:
            app.redis.set(key, dumps(rv))
            app.redis.expire(key, rv_ttl)