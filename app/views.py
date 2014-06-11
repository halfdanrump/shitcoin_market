from app import flapp, socketio, oid
from flask import render_template, redirect, flash, g, session, request, url_for, flash
from forms import OrderForm, UserLoginForm, UserRegisterForm
from app.dbase.models import User
from app import logger
#book = Orderbook(app)
#book.start_auction()
#log.setLevel(logging.DEBUG)


@flapp.before_request
def lookup_current_user():
	
	g.user = None
	if 'openid' in session:
		openid = session['openid']
		g.user = User.query.filter_by(openid = openid).first()
	print 'CURRENT USER:', g.user

@flapp.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None:
		return redirect( oid.get_next_url() )
	
	if request.method == 'POST':
		openid = request.form.get('openid')
		if openid: 
			return oid.try_login(openid, ask_for=['email'])
    
	return render_template('login.html', next=oid.get_next_url(), error=oid.fetch_error())




@oid.after_login
def create_or_login(response):
	session['openid'] = response.identity_url
	logger.debug( 'OpenID login with identity_url: %s'%response.identity_url )
	user = User.query.filter_by(openid=response.identity_url).first()
	logger.debug( 'Matched openid with registered user: %s'%user )
	if user is not None:
		g.user = user
		logger.debug( 'User signed in %s'%user )
		flash(u'Successfully signed in')
		logger.debug( 'Redirecting to URL: %s'%oid.get_next_url())
		return redirect(oid.get_next_url())
	# else:
	# 	logger.debug( 'User not registered in system: %s'%response.identity_url )
	
	# register_form = UserRegisterForm()
	
	# if register_form.validate_on_submit():
	# 	g.user = User.create(openid = response.identity_url, **form.data)
	# 	logger.debug( 'Created user %s'%g.user )
	# # return render_template("create_profile.html", identity_url = response.identity_url, register_form = register_form)
	return redirect( url_for( 'create_profile', next=oid.get_next_url(), identity_url = response.identity_url) )

import uuid
@flapp.route('/create_profile', methods = ['GET', 'POST'])
def create_profile():
	register_form = UserRegisterForm()
	logger.debug('IN CREATE PROFILE1')
	logger.debug('OPENID: %s'%session['openid'])
	logger.debug('GLOBAL USER: %s'%g.user)
	if g.user is not None or 'openid' not in session:
		logger.debug( 'Redicredting user %s to home screen...'%g.user)
		return redirect(url_for('home'))
	
	if register_form.validate_on_submit():
		new_user = User.create(openid = uuid.uuid4().hex, name = 'Halfdan')
		logger.debug( 'Creating new user %s'%new_user )
		g.user = new_user
		logger.debug( oid.get_next_url())
		return redirect( oid.get_next_url())
	logger.debug('IN CREATE PROFILE2')
	return render_template("create_profile.html", register_form = register_form, next = oid.get_next_url())


@flapp.route('/submit_form', methods = ['POST'])
def fuckface():
	logger.debug('FUCKFACE')
	return render_template('dummy.html')


@flapp.route('/', methods = ['GET'])
def index():
	return redirect(url_for('login'))


	



@flapp.route('/home', methods = ['GET', 'POST'])
def home():
	if g.user:
		logger.debug('Taking logged in user to home screen %s'%g.user)
		order_form = OrderForm()
		buy_side, sell_side = flapp.orderbooks['book_1'].get_cumulative_book(as_json = True)
		return render_template("index.html", order_form = order_form, auction_id = 'orderbook_id_1')
	else:
		flash('Please login before going to home screen')
		return redirect(url_for('login'))


