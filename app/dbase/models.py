from app import db
from sqlalchemy.types import Enum

class DBOrder(db.Model):
	id = db.Column( db.Integer, primary_key = True )
	uuid = db.Column( db.String(length = 32), unique = True, primary_key = True )
	price = db.Column( db.Integer )
	volume = db.Column( db.Integer )
	received = db.Column ( db.DateTime )
	order_type = db.Column( db.String(length = 6) )
	side = db.Column( db.String(length = 4) )
	owner = db.Column( db.String(length = 32) )

	def __init__(self, **kwargs):
		self.uuid = kwargs['uuid'].hex
		self.price = kwargs['price']
		self.volume = kwargs['volume']
		self.received = kwargs['received']
		self.order_type = kwargs['order_type']
		self.side = kwargs['side']
		self.owner = kwargs['owner']
