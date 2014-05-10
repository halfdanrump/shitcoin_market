from app.testing.orderbook import BasicOrderbookTests
from app import flapp, db
import unittest

if __name__ == "__main__":
	flapp.config.from_object('app.config.app_config.TestConfig')
	unittest.main()