from app import flapp
from redis import Redis

def clear_redis_keys(setup_func):
	"""
	Decorator to clear redis keys before tests. Apply this decorator to the setUp method of a test class.
	"""
	def with_redis_initialization(test_class):
		flapp.config.from_object('app.config.app_config.TestConfig')
		
		print 'Clearing database for environmet %s'%flapp.config['REDIS_PREFIX']
		
		rcon = Redis()
		keys = rcon.keys(flapp.config['REDIS_PREFIX'] + '*')
		for key in keys:
			print 'Deleting key %s'%key
			rcon.delete(key)
		
		setup_func(test_class)
		return setup_func

	return with_redis_initialization