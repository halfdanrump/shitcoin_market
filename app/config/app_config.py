import os
class BaseConfig():
	SRF_ENABLED = True
	SECRET_KEY = os.urandom(16)
	JSON_DATETIME_FORMAT = '%Y-%m-%d-%H:%M'

class TestConfig(BaseConfig):
	DEBUG = True
	REDIS_PREFIX = 'test'
	LOGFILE = ''

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	REDIS_PREFIX = 'development'

class ProductionConfig(BaseConfig):
	DEBUG = False
	REDIS_PREFIX = 'production'