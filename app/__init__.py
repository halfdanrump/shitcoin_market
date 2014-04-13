from flask import Flask
from redis import Redis
from market.orderbook import Orderbook

app = Flask(__name__)

### Redis setup
app.redis = Redis()
app.config['order_queue'] = 'my_queue'



### Create market objects
book = Orderbook()

# from app import config
# app.config.from_object(config.app_config)

### Create SocketIO wrapper for 

from flask.ext.socketio import SocketIO
socketio = SocketIO(app)

from app import views, market