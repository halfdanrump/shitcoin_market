from app import app
#from app.market.messages import Order
from flask import render_template
import logging
from market import utils, Orderbook, orderbook


orderlog = logging.getLogger('orderlog')
book = Orderbook()

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
	rv = orderbook.process_order.queue_order(order)
	print rv.return_value
	#best_prices = orderbook.process_order.receive_order(order)
	callback = render_template("index.html")
	return callback

