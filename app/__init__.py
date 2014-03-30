from flask import Flask
from redis import Redis
from market.orderbook import Orderbook

app = Flask(__name__)
app.redis = Redis()
app.config['order_queue'] = 'my_queue'

book = Orderbook()

from app import views, market