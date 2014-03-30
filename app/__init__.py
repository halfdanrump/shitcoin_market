from flask import Flask
from redis import Redis
from market.orderbook import Orderbook

app = Flask(__name__)
app.redis = Redis()
app.config['order_queue'] = 'my_queue'

import logging.config, yaml
config = yaml.load(open('app/config/log_conf.yaml'))
logging.config.dictConfig(config)
# l = logging.getLogger(__name__)
# l.error('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTEEEEEEEEEEEEEEEEEEEEEEEEE')

# from logging.handlers import RotatingFileHandler
# import logging

# handler = RotatingFileHandler('logs/app.log', maxBytes = 10000)
# handler.setLevel(logging.INFO)
# app.logger.addHandler(handler)


book = Orderbook()

from app import views, market