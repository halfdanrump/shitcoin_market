from flask import Flask
from redis import Redis
from market.orderbook import Orderbook

app = Flask(__name__)
print __name__
app.redis = Redis()
app.config['order_queue'] = 'my_queue'

# import logging.config, yaml
# config = yaml.load(open('log_conf.yaml'))
# logging.config.dictConfig(config)
# l = logging.getLogger(__name__)
# l.error('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTEEEEEEEEEEEEEEEEEEEEEEEEE')

import logging
error_handler = logging.FileHandler('errors.log')
error_handler.setLevel(logging.ERROR)
app.logger.addHandler(error_handler)

book = Orderbook()

from app import views, market