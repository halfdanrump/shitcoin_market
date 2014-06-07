from app import flapp, socketio
from flask import render_template, redirect, flash
from forms import OrderForm, UserLoginForm


#book = Orderbook(app)
#book.start_auction()
#log.setLevel(logging.DEBUG)


@flapp.route('/', methods = ['GET'])
def login():
	login_form = UserLoginForm()
	return render_template("login.html", login_form = login_form)


@flapp.route('/home', methods = ['GET'])
def index():
	order_form = OrderForm()
	# if order_form.validate_on_submit():
	# 	### Create order object form form data
	# 	order_data = dict(**order_form.data)
	# 	order_data['created'] =  datetime.utcnow()
		
	# 	flash('Submitted order: %s'%order_data)
	# 	return redirect('/')
	buy_side, sell_side = flapp.orderbooks['book_1'].get_cumulative_book(as_json = True)
	print buy_side, sell_side
	return render_template("index.html", order_form = order_form, auction_id = 'orderbook_id_1')

