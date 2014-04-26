from app import app, socketio, rcon
#from app.market.messages import Order
from flask import render_template, redirect, flash
import logging
from market import utils, Orderbook
from market.messages import Order
from forms import OrderForm
from market.orderbook import queue_order
from market.utils import verify_order_data, error_handler
import urlparse
from flask.ext.socketio import emit

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
		
		flash('Submitted order: %s'%order_data)
		return redirect('/')

	return render_template("index.html", order_form = order_form)

@error_handler
@socketio.on('order submitted', namespace = '/test')
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