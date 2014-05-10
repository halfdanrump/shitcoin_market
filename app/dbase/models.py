from app import db

class DBOrder(db.Model):
	id = db.Column( db.Integer, primary_key = True )
	uuid = db.Column( db.String(32), unique = True )
	price = db.Column( db.Integer )
	volume = db.Column( db.Integer )

	def __init__(self, **kwargs):
		self.uuid = kwargs['uuid']
		self.price = kwargs['price']
		self.volume = kwargs['volume']