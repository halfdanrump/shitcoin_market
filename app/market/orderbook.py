import Queue
import logging


from flask import current_app
from pickle import loads, dumps

from uuid import uuid4

def queue_daemon(app, rv_ttl=500):
	while True:
	    msg = app.redis.blpop(app.config['order_queue'])
	    app.logger.info('Popped order from queue')
	    func, key, args, kwargs = loads(msg[1])
	    try:
	        rv = func(*args, **kwargs)
	    except Exception, e:
	        rv = e
	    if rv is not None:
	        app.redis.set(key, dumps(rv))
        	app.redis.expire(key, rv_ttl)


class DelayedResult(object):
    def __init__(self, key):
        self.key = key
        self._rv = None

    @property
    def return_value(self):
        if self._rv is None:
            rv = current_app.redis.get(self.key)
            if rv is not None:
                self._rv = loads(rv)
        return self._rv


def queuefunc(f):
    def queue_order(*args, **kwargs):
        qkey = current_app.config['order_queue']
        key = '%s:result:%s' % (qkey, str(uuid4()))
        s = dumps((f, key, args, kwargs))
        print current_app.redis.rpush(current_app.config['order_queue'], s)
        return DelayedResult(key)
    f.queue_order = queue_order
    return f

@queuefunc
def process_order(order):
	print order
	pass
	#print 'Processing order %s'%order
	#return 'Processing complete message'

class Orderbook():
	
	#orderlog = logging.getLogger('orderlog')

	ID = 0

	def __init__(self):
		self.ID += 1
		self.buy_orders = Queue.PriorityQueue()
		self.sell_orders = Queue.PriorityQueue()
		

	
		# if order.is_limit():
		# 	if order.is_buy():
		# 		print order.get_details()
		# 		self.buy_orders.put()

		# 	elif order.side == order.SELL:
		# 		print order.get_details()
		# 	else:
		# 		raise Exception('Order side was not specified')
		# elif order.type == 'MARKET':
		# 	pass
		# else:
		# 	raise Exception('Order type was not specified')
		
		

		# return {'best_buy':0, 'best_sell':0}