from app import flapp

from redis import Redis
import unittest

# class TestInitDecorator(object):
# 	def __init__(self):
		

def clear_redis_keys():
	"""
	Removes all keys with the Test prefix
	"""
	print 'Clearing database for environmet %s'%flapp.config['REDIS_PREFIX']
	rcon = Redis()
	keys = rcon.keys(flapp.config['REDIS_PREFIX'] + '*')
	for key in keys:
		print 'Deleting key %s'%key
		rcon.delete(key)


class MarketTester(unittest.TestCase):
    def setUp(self):
        flapp.config.from_object('app.config.app_config.TestConfig')
        clear_redis_keys()