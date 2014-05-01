from flask_wtf import Form
from wtforms import IntegerField, SelectField, RadioField
from wtforms.validators import Required
from market.messages import Order

class OrderForm(Form):
	price = IntegerField(label = 'price', validators = [Required()])
	volume = IntegerField(label = 'volume', validators = [Required()], default = 10)
	side = RadioField(label = 'side', validators = [Required()], choices = [(Order.BUY, 'Buy'), (Order.SELL, 'Sell')])
	type = SelectField(label = 'type', validators = [Required()], choices = [(Order.LIMIT, 'Limit order'), (Order.MARKET, 'Market order')])
