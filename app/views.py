from app import flapp, socketio, oid
from flask import render_template, redirect, flash, g, session, request, url_for
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

from flask import flash


@oid.after_login
def create_or_login(response):
	session['openid'] = response.identity_url
	logger.debug( 'OpenID login with identity_url: %s'%response.identity_url )
	user = User.query.filter_by(openid=response.identity_url).first()
	if user:
		g.user = user
		logger.debug( 'User signed in %s'%user )
		# flash(u'Successfully signed in')
		return redirect(oid.get_next_url())
	else:
		logger.debug( 'User not registered in system: %s'%response.identity_url )
		register_form = UserRegisterForm()
		if register_form.validate_on_submit():
			g.user = User.create(openid = response.identity_url, **form.data)
			logger.debug( 'Created user %s'%g.user )
		return render_template("create_profile.html", identity_url = response.identity_url, register_form = register_form)
		# return redirect( url_for( 'create_profile', next=oid.get_next_url(), identity_url = response.identity_url) )


# @flapp.route('/create_profile', methods = ['GET', 'POST'])
# def create_profile():
# 	if g.user:# or 'openid' not in session:
# 		logger.debug( 'Redicredting user %s to home screen...'%g.user)
# 		return redirect(url_for('home'))
# 	else:
# 		logger.debug( 'Redirecting unknown user to create profile page %s'%identity_url[])
# 		return render_template("create_profile.html")


@flapp.route('/', methods = ['GET'])
def index():
	return redirect(url_for('login'))


@flapp.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	login_form = UserLoginForm()
	if g.user is not None:
		return redirect( oid.get_next_url() )
	
	if request.method == 'POST':
		openid = request.form.get('openid')
		if openid: 
			return oid.try_login(openid, ask_for=['email'])
    
	return render_template('login.html', next=oid.get_next_url(), error=oid.fetch_error(), login_form = login_form)
	# if login_form.validate_on_submit():
	# 	return redirect('/home')

	# return render_template("login.html", login_form = login_form, providers = flapp.config['OPENID_PROVIDERS'])




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


