from app import flapp, login_manager
from app.dbase.models import User


def prefixed(redis_key):
	return flapp.config['REDIS_PREFIX'] + '_' + redis_key

@login_manager.user_loader
def load_user(userid):
	try:
		return User.query.get(int(userid))
	except:
		return None