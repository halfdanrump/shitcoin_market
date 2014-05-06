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

# @FocusDecorator
# def test1():
# 	print 'Running test 1'		

if __name__ == "__main__":
	print 'active'
	print active
	run_tests()