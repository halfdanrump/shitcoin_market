from flask.ext.socketio import emit
from app import logger
from app import socketio


from datetime import datetime
import cPickle
def queue_order(redis, auction_id, order_data):
	logger.debug('Received order: %s'%order_data)
	order_data['received'] = datetime.utcnow()
	redis.rpush(auction_id, cPickle.dumps(order_data))


from app import rcon
import urlparse
from app.market.utils import verify_order_data, error_handler
@socketio.on('order submitted', namespace = '/client')
def order_placed(query_string):
	def convert_to_dict(order_form):
		return dict([(k, v[0]) for k, v in order_form.items()])
	try:
		order_data = urlparse.parse_qs(query_string['data'])
		order_data.pop('csrf_token')
		order_data = convert_to_dict(order_data)
		order_valid, message = verify_order_data(order_data)
		emit('order validation', message)
		if order_valid:
			queue_order(rcon, 'book_1', order_data)
	except Exception, e:
		print e

def transmit_book_to_client(orderbook):
	# try:
		buy_side, sell_side = orderbook.get_cumulative_book(as_json = True)
		print buy_side, sell_side
		socketio.emit('orderbook update', 
					{'buy_side':buy_side, 'sell_side': sell_side}, 
					namespace='/client')
		logger.debug('Sent orderbook volume to client')
	# except Exception, e:
	# 	logger.debug('asdasd')
	# 	logger.debug(e)

def invalid_message(exception):
	logger.exception(exception)

# @socketio.on('order receive success', namepace = '/client')
# def 