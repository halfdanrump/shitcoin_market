from app import app, socketio, rcon
#from app.market.messages import Order
from flask import render_template, redirect, flash
import logging
from market import utils, Orderbook
from market.orderbook import error_handler
from market.messages import Order
from forms import OrderForm
from market.orderbook import queue_order
from datetime import datetime


orderlog = logging.getLogger('orderlog')
#book = Orderbook(app)
#book.start_auction()
#log.setLevel(logging.DEBUG)


@app.route('/', methods = ['GET', 'POST'])
def index():
	order_form = OrderForm()
	if order_form.validate_on_submit():
		### Create order object form form data
		order_data = dict(**order_form.data)
		order_data['created'] =  datetime.utcnow()
		queue_order(rcon, 'book_1', order_data)
		flash('Submitted order: %s'%order_data)

		return redirect('/')
	return render_template("index.html", order_form = order_form)

@app.route('/order', methods = ['POST'])
def order():
	order = utils.get_random_order()
	queue_order(redis, 'order', book_1)
	#print rv.return_value
	#best_prices = orderbook.process_order.receive_order(order)
	return redirect('/')

# @app.route('/start', methods = ['POST'])
# def start_auction():
# 	book.start_auction(app)
# 	return redirect('/')

# @app.route('/restart', methods = ['POST'])
# def restart_auction():
# 	book.restart_auction(app)
# 	return redirect('/')