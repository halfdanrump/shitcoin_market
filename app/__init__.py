from flask import Flask
from redis import Redis
from market.orderbook import Orderbook

app = Flask(__name__)
app.config.from_object('config')

### Redis setup
app.redis = Redis()
app.config['order_queue'] = 'my_queue'


### Create market objects
book = Orderbook()

from app import views, market