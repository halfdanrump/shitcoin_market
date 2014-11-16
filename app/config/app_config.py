import os
basedir = os.path.abspath(os.path.join(os.path.split(os.path.dirname(__file__))[:-1])[0])

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')








class BaseConfig():
	CSRF_ENABLED = True
	SECRET_KEY = os.urandom(16)
	JSON_DATETIME_FORMAT = '%Y-%m-%d-%H:%M'
	PSQL_ROLE = 'halfdan'
	OPENID_PROVIDERS = [
    	{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
	    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
	    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
	    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
	    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }
	    ]

	USER_START_WEALTH = 10000
	MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'shitcoinmarket@gmail.com')
	MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'a54a425452244d37ae86121d6dc46fa4')
	MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <shitcoinmarket@gmail.com>')
	MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
	MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
	MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))


class TestConfig(BaseConfig):
	DEBUG = True
	REDIS_PREFIX = 'test'
	PSQL_DATABASE = 'shitcoin_test'
	SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/shitcoin_test"
	LOGFILE = ''
	PORT = 5001

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	REDIS_PREFIX = 'development'
	PSQL_DATABASE = 'shitcoin_dev'
	SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/shitcoin_dev"
	PORT = 5000

class ProductionConfig(BaseConfig):
	DEBUG = False
	REDIS_PREFIX = 'production'
	PSQL_DATABASE = 'shitcoin_prod'
	SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/shitcoin_prod"
	PORT = 80