from flask_wtf import Form
from wtforms import IntegerField, SelectField, RadioField
from wtforms.validators import Required
from app.dbase.models import Order

class OrderForm(Form):
	price = IntegerField(label = 'price', validators = [Required()])
	volume = IntegerField(label = 'volume', validators = [Required()], default = 10)
	side = RadioField(label = 'side', validators = [Required()], choices = [(Order.BUY, 'Buy'), (Order.SELL, 'Sell')])
	order_type = SelectField(label = 'order_type', validators = [Required()], choices = [(Order.LIMIT, 'Limit order'), (Order.MARKET, 'Market order')])
