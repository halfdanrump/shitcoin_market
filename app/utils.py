from app import flapp


def prefixed(redis_key):
	return flapp.config['REDIS_PREFIX'] + '_' + redis_key
