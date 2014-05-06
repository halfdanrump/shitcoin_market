import unittest
from app import flapp

active = list()

def run_tests():
    for test in active:
        test()

class FocusDecorator(object):
    def __init__(self, test):
        self.test = test
        active.append(self)
    def __call__(self):
        print '(focus = True) ' + self.test.__name__


from orderbook import *

if __name__ == "__main__":
	print 'active'
	print active
	run_tests()