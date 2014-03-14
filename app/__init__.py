from flask import Flask
from redis import Redis

app = Flask(__name__)
app.redis = Redis()
app.config['order_queue'] = 'my_queue'
from app import views, market