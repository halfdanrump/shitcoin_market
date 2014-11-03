from app.dbase.models import User
from app import user_manager
from uuid import uuid4
from datetime import datetime


class UserFactory(object):

	@staticmethod
	def seed_confirmed_user(username, password):
		return User.create(username=username, is_enabled=True, password=user_manager.hash_password(password), confirmed_at = datetime.now())

	@staticmethod
	def seed_nonconfirmed_user(username, password):
		return User.create(username=username, is_enabled=False, password=user_manager.hash_password(password))