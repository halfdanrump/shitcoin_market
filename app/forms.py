from flask_wtf import Form
from wtforms import IntegerField, SelectField, RadioField, SubmitField, TextField, BooleanField, PasswordField
from wtforms.validators import DataRequired, length
from app.dbase.models import Order
import random

class OrderForm(Form):
	price = IntegerField(label = 'price', validators = [DataRequired()])
	volume = IntegerField(label = 'volume', validators = [DataRequired()], default = 10)
	side = RadioField(label = 'side', validators = [DataRequired()], choices = [(Order.BUY, 'Buy'), (Order.SELL, 'Sell')])
	order_type = SelectField(label = 'order_type', validators = [DataRequired()], choices = [(Order.LIMIT, 'Limit order'), (Order.MARKET, 'Market order')])
	submit_button = SubmitField('Place order!')


class UserRegisterForm(Form):
	nickname = TextField(label = 'nickname', validators = [DataRequired(), length(min = 3, max = 50, message = 'Username must be between 6 and 50 characters')])
	submit_button = SubmitField('Sign up!')
	def validate_name(self, name):
		return True


class UserLoginForm(Form):
	openid = TextField(label = 'openid', default = 'https://www.google.com/accounts/o8/id')
	nickname = TextField(label = 'nickname')
	password = PasswordField(label = 'password')
	remember_me = BooleanField(label = 'remember me', default = False)
	submit_button = SubmitField('Sign in!')