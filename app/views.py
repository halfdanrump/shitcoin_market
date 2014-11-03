from app import flapp, socketio, oid
from flask import render_template, redirect, flash, g, session, request, url_for, flash
from forms import OrderForm, UserLoginForm, UserRegisterForm
from app.dbase.models import User
from app import logger
import uuid
from flask_user import login_required, current_user

# @flapp.before_request
# def lookup_current_user():
# 	g.user = None
# 	if 'openid' in session:
# 		# logger.debug('OPENID IN SESSION')
# 		openid = session['openid']
# 		g.user = User.query.filter_by(openid = openid).first()
# 	# logger.debug('BEFORE REQUEST wit1 url: %s, user: %s'%(request.url, g.user))



# @flapp.route('/', methods = ['GET'])
# def index():
	
# 	return render_template('home.html')
# 	# return redirect('/home')
# 	# return 'YAY'
# 	# print g.user
	
# 	# if g.user is None: 
# 	# 	return redirect(url_for('login'))
# 	# else: 
# 	# 	return redirect(url_for('home'))


@flapp.route('/test', methods = ['GET'])
@login_required
def testroute():
	print flapp.config.get('TESTING')
	return 'YES!'

@flapp.route('/', methods = ['GET', 'POST'])
@login_required
def home():
	order_form = OrderForm()
	buy_side, sell_side = flapp.orderbooks['book_1'].get_cumulative_book(as_json = True)
	return render_template(
			"home.html", 
			order_form = order_form, 
			auction_id = 'orderbook_id_1',
			user = current_user,
			sign_out_url = flapp.config['USER_LOGOUT_URL']
			)
	# else:
	# 	flash('Please login before going to home screen')
	# 	# return 'WOOOOOOO'
	# 	return redirect(url_for('login'))


# @flapp.route('/login', methods = ['GET'])
# def login():
# 	if not g.user is None and g.user.is_authenticated():
# 		redirect( url_for('home') )
# 	else:
# 		username = request.form.get('username')
# 		username = request.form.get('password')

# @flapp.route('/login', methods = ['GET', 'POST'])
# @oid.loginhandler
# def login_with_openid():
# 	if not g.user is None and g.user.is_authenticated():
# 		return redirect( oid.get_next_url() )
# 	else:
# 		login_form = UserLoginForm()
# 		if login_form.validate_on_submit():
# 			openid = request.form.get('openid')
# 			session['remember_me'] = login_form.remember_me.data
# 			return oid.try_login(openid, ask_for = ['email'])
# 		else:
# 			return render_template('login.html', login_form = login_form)

# @flapp.route('/logout', methods = ['GET'])
# def logout():
# 	session.pop('openid', None)
# 	flash('You logged out')
# 	return redirect(oid.get_next_url())


# @oid.after_login
# def login_or_create(response):
# 	session['openid'] = response.identity_url
# 	user = User.query.filter_by(openid=response.identity_url).first()
# 	if user is not None:
# 		g.user = user
# 		return redirect(oid.get_next_url())
# 	else:
# 		return redirect( url_for('create_profile', next=oid.get_next_url(), openid = session['openid']) )


# @flapp.route('/create_profile', methods = ['GET', 'POST'])
# def create_profile():
# 	logger.debug(session)
# 	if g.user is not None or 'openid' not in session:
# 		logger.debug( 'Redicredting user %s to home screen...'%g.user)
# 		return redirect('/')
# 	else:
# 		register_form = UserRegisterForm()
# 		if register_form.validate_on_submit():
# 			new_user = User.create(username = register_form.username.data, openid = session['openid'])
# 			logger.debug( 'Creating new user %s'%new_user )
# 			g.user = new_user
# 			logger.debug( oid.get_next_url())
# 			return redirect( oid.get_next_url())
# 		else:
# 			return render_template('create_profile.html', register_form = register_form, next = oid.get_next_url())




	





