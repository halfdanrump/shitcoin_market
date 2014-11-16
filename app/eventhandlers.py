from flask.ext.socketio import emit
from app import socketio, flapp, logger, rcon
from app.utils import prefixed
from datetime import datetime
import cPickle
import urlparse
from app.market.utils import verify_order_data

def queue_order(redis, auction_id, order_data):
	logger.debug('Received order: %s'%order_data)
	order_data['received'] = datetime.utcnow()
	redis.rpush(prefixed(auction_id), cPickle.dumps(order_data))


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

@flapp.route('/order/new')
def submit_new_order():
	pass
# @socketio('client requests order history')
# def transmit_order_history_to_use():
	

# @socketio.on('client requests orderbook status', namespace = '/client')
# def transmit_book_to_client(book = None):
	
# 	if not book:
# 		book = flapp.book
		
# 	buy_side, sell_side = book.get_cumulative_book(as_json = True)

# 	logger.info(buy_side)
# 	socketio.emit('orderbook update', 
# 				{'buy_side':buy_side, 'sell_side': sell_side}, 
# 				namespace='/client')
# 	logger.debug('Sent orderbook volume to client')
	
import json
@socketio.on('client requests orderbook status', namespace = '/client')
def transmit_book_to_client(rkey = None):
	logger.warning('RKEY:::::::::::::::%s'%rkey)
	cumulative_book = rcon.get(rkey)
	logger.warning('CUMULATIVE BOOK %s'%cumulative_book)
	logger.warning('CUMULATIVE BOOK %s'%type(cumulative_book))
	try:
		buy_side, sell_side = json.loads(rcon.get(rkey))
		socketio.emit('orderbook update', 
				{'buy_side':buy_side, 'sell_side': sell_side}, 
				namespace='/client')
		logger.debug('Sent orderbook volume to client')
	except TypeError, ValueError:
		logger.exception('OADIJOASIDJAOISDJOASIJDOASIDJ')

	
