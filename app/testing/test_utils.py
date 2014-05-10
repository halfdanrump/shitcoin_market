from app import flapp, db
from redis import Redis

def init_db(setup_func):
	def recreate_schema(test_class):
		print 'Re-creating db schema for environmet %s'%flapp.config['REDIS_PREFIX']
		db.drop_all()
		db.create_all()
		setup_func(test_class)
		return setup_func
	return recreate_schema

def clear_redis_keys(setup_func):
	"""
	Decorator to clear redis keys before tests. Apply this decorator to the setUp method of a test class.
	"""
	def with_redis_initialization(test_class):
				
		print 'Cleaning Redis for environmet %s'%flapp.config['REDIS_PREFIX']
		
		rcon = Redis()
		keys = rcon.keys(flapp.config['REDIS_PREFIX'] + '*')
		for key in keys:
			print 'Deleting key %s'%key
			rcon.delete(key)

		setup_func(test_class)
		return setup_func

	return with_redis_initialization