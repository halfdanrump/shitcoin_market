from app import flapp, socketio
from flask import render_template, redirect, flash
from forms import OrderForm


#book = Orderbook(app)
#book.start_auction()
#log.setLevel(logging.DEBUG)


@flapp.route('/', methods = ['GET'])
def index():
	order_form = OrderForm()
	# if order_form.validate_on_submit():
	# 	### Create order object form form data
	# 	order_data = dict(**order_form.data)
	# 	order_data['created'] =  datetime.utcnow()
		
	# 	flash('Submitted order: %s'%order_data)
	# 	return redirect('/')
	buy_side, sell_side = flapp.book.get_cumulative_book(as_json = True)
	print buy_side, sell_side
	return render_template("index.html", order_form = order_form, auction_id = 'auction_1')

