from app.market.utils import verify_order_data, error_handler
import urlparse
from flask.ext.socketio import emit
from app import logger
from app import socketio
from redis import Redis

def queue_order(redis, auction_id, order_data):
	logger.debug('Received order: %s'%order_data)
	order_data['received'] = datetime.utcnow()
	s = dumps(order_data)
	r = Redis()
	r.rpush(auction_id, s)


@socketio.on('order submitted', namespace = '/client')
def order_placed(query_string):
	try:
		order_data = urlparse.parse_qs(query_string['data'])
		order_data.pop('csrf_token')
		order_data = dict([(k, v[0]) for k, v in order_data.items()])
		if verify_order_data(order_data):
			queue_order(rcon, 'book_1', order_data)
			emit('order receive success')
		else:
			emit('order receive failure')
	except Exception, e:
		print e

@socketio.on('orderbook update', namespace = '/client')
def transmit_book_to_client(orderbook):
	try:
		buy_side, sell_side = orderbook.get_cumulative_book()
		socketio.emit('orderbook update', 
					{'buy_side':buy_side, 'sell_side': sell_side}, 
					namespace='/client')
		logger.debug('Sent orderbook volume to client')
	except Exception, e:
		logger.debug(e)
