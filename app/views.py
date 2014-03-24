from app import app, book
#from app.market.messages import Order
from flask import render_template
import logging
from market import utils, Orderbook
from market.orderbook import error_handler


orderlog = logging.getLogger('orderlog')
#book = Orderbook(app)
#book.start_auction()
#log.setLevel(logging.DEBUG)

@app.route('/', methods = ['GET'])
def index():
	#order = utils.get_random_order()
	#best_prices = orderbook.process_order.receive_order(order)
	callback = render_template("index.html")
	return callback

@app.route('/order', methods = ['POST'])
def order():
	order = utils.get_random_order()
	rv = book.process_order.queue_order(order)
	#print rv.return_value
	#best_prices = orderbook.process_order.receive_order(order)
	callback = render_template("index.html")
	return callback

@app.route('/start', methods = ['POST'])
def start_auction():
	book.start_auction(app)
	callback = render_template("index.html")
	return callback