from tester import FocusDecorator, run_tests, active
from app.market.orderbook import Orderbook

@FocusDecorator
def test1():
        print 'Running test 1'

@FocusDecorator
def test2():
        print 'Running test 2'
