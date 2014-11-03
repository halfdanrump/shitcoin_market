import unittest
from app import flapp, socketio, user_manager
from splinter import Browser
from flask import url_for
from app.dbase.models import User
from uuid import uuid4
from datetime import datetime
from factories import UserFactory

class TestRoutes(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		socketio.run(flapp, port = flapp.config['PORT'])
		pass
		

	def setUp(self):
		self.browser = Browser()
		self.username = uuid4().hex
		self.userpassword = uuid4().hex

	def tearDown(self):
		self.browser.quit()
		
	def go_home(self):
		self.browser.visit( 'http://localhost:%s'%flapp.config['PORT'])

	def login(self, user):
		self.go_home()
		self.browser.fill_form({'username': self.username, 'password':self.userpassword})
		self.browser.find_by_value('Sign in').click()


	def test_login_success_with_confirmed_user(self):
		self.login(UserFactory.seed_confirmed_user(self.username, self.userpassword))
		assert self.browser.is_text_present('Signed in as %s'%self.username)


	def test_login_failure_with_nonconfirmed_user(self):
		user = UserFactory.seed_nonconfirmed_user(self.username, self.userpassword)
		self.login(user)
		assert self.browser.is_text_not_present('Signed in as %s'%self.userpassword)
		assert self.browser.is_text_present('Sign in')

	def test_login_failure_with_nonexisting_user(self):
		self.go_home()
		fake_username = uuid4().hex
		self.browser.fill_form({'username': fake_username, 'password':uuid4().hex})
		self.browser.find_by_value('Sign in').click()
		assert self.browser.is_text_not_present('Signed in as %s'%fake_username)
		assert self.browser.is_text_present('Sign in')

	def test_logout(self):
		self.login(UserFactory.seed_confirmed_user(self.username, self.userpassword))
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