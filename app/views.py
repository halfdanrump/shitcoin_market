from app import flapp, socketio, oid
from flask import render_template, redirect, flash, g, session, request, url_for, flash
from forms import OrderForm, UserLoginForm, UserRegisterForm
from app.dbase.models import User
from app import logger
import uuid

@flapp.before_request
def lookup_current_user():
	
	g.user = None
	if 'openid' in session:
		openid = session['openid']
		g.user = User.query.filter_by(openid = openid).first()
	logger.debug('BEFORE REQUEST: ', g.user)


@flapp.route('/', methods = ['GET'])
def index():
	print 'UUUUUUUUUUUUUUSER'
	print g.user

	if g.user is None: 

		return redirect(url_for('login'))
	else: 
		return redirect( url_for('home') )


@flapp.route('/home', methods = ['GET', 'POST'])
def home():
	if g.user:
		logger.debug('Taking logged in user to home screen %s'%g.user)
		order_form = OrderForm()
		buy_side, sell_side = flapp.orderbooks['book_1'].get_cumulative_book(as_json = True)
		return render_template("home.html", order_form = order_form, auction_id = 'orderbook_id_1')
	else:
		flash('Please login before going to home screen')
		return redirect(url_for('login'))


@flapp.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	
	if g.user is not None and g.user.is_authenticated():
		return redirect( oid.get_next_url() )
	
	login_form = UserLoginForm()

	if login_form.validate_on_submit():
		openid = request.form.get('openid')
		session['remember_me'] = login_form.remember_me.data
		return oid.try_login(openid)

	return render_template('login.html', login_form = login_form)



@oid.after_login
def login_or_create(response):
	session['openid'] = response.identity_url
	logger.debug( 'Login with openid: %s'%session['openid'] )
	user = User.query.filter_by(openid=response.identity_url).first()
	logger.debug( 'Matched openid with registered user: %s'%user )

	if user is not None:
		g.user = user
		logger.debug( 'User signed in %s'%user )
		flash('Successfully signed in')
		logger.debug('Redirecting to URL: %s'%oid.get_next_url())
		return redirect(oid.get_next_url())
	
	return redirect( url_for('create_profile', next=oid.get_next_url(), openid = session['openid']) )


@flapp.route('/create_profile', methods = ['GET', 'POST'])
def create_profile():
	
	logger.debug(session)
	if g.user is not None or 'openid' not in session:
		logger.debug( 'Redicredting user %s to home screen...'%g.user)
		return redirect('/')
	
	register_form = UserRegisterForm()
	if register_form.validate_on_submit():
		new_user = User.create(username = register_form.nickname.data, openid = session['openid'])
		logger.debug( 'Creating new user %s'%new_user )
		g.user = new_user
		logger.debug( oid.get_next_url())
		return redirect( oid.get_next_url())
	
	logger.debug('RENDERING CREATE PROFILE PAGE')
	return render_template('create_profile.html', register_form = register_form, next = oid.get_next_url())




	





