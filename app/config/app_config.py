import os
class BaseConfig():
	SRF_ENABLED = True
	SECRET_KEY = os.urandom(16)
	JSON_DATETIME_FORMAT = '%Y-%m-%d-%H:%M'
	PSQL_ROLE = 'halfdan'

class TestConfig(BaseConfig):
	DEBUG = True
	REDIS_PREFIX = 'test'
	PSQL_DATABASE = 'shitcoin_test'
	SQLALCHEMY_DATABASE_URI = "postgresql://halfdan@localhost/shitcoint_test"
	LOGFILE = ''

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	REDIS_PREFIX = 'development'
	PSQL_DATABASE = 'shitcoin_dev'
	SQLALCHEMY_DATABASE_URI = "postgresql://halfdan@localhost/shitcoint_dev"

class ProductionConfig(BaseConfig):
	DEBUG = False
	REDIS_PREFIX = 'production'
	PSQL_DATABASE = 'shitcoin_prod'
	SQLALCHEMY_DATABASE_URI = "postgresql://halfdan@localhost/shitcoint_prod"