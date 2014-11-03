import unittest
from app import flapp, socketio, user_manager
from splinter import Browser
from flask import url_for
from app.dbase.models import User
from uuid import uuid4
from datetime import datetime

class TestRoutes(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# socketio.run(flapp, port = 8080)
		pass
		

	def setUp(self):
		self.browser = Browser()
		self.username = uuid4().hex
		self.userpassword = uuid4().hex
		self.user = User.create(username=self.username, is_enabled=True, password=user_manager.hash_password(self.userpassword), confirmed_at = datetime.now())

	def tearDown(self):
		self.browser.quit()
		
	def login(self):
		self.browser.visit( 'http://localhost:5000')
		self.browser.fill_form({'username': self.username, 'password':self.userpassword})
		self.browser.find_by_value('Sign in').click()

	def test_login_with_confirmed_user(self):
		self.login()
		assert self.browser.is_text_present('Signed in as %s'%self.username)

	def test_logout(self):
		self.login()
		self.browser.click_link_by_text('Sign out')
		assert self.browser.is_text_not_present('Signed in as %s'%self.username)
		assert self.browser.is_text_present('Sign in')

	# def test_index(self):
	# 	r = flapp.get('/')
	# 	assert r.okbr

	# def test_login_with_id(self):
	# 	self.login()
	# 	print self.browser.html
	# 	# print browser.html

# class TestRoutesHeadless(unittest.TestCase):

# 	def setUp(self):
# 		self.browser 