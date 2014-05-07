import logging.config, logging.handlers, yaml
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
handler = logging.handlers.RotatingFileHandler('orderbook.log', maxBytes = 10**6)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('\n\n#################Starting server!#################\n')

from flask import Flask
flapp = Flask(__name__)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

flapp.orderbooks = dict()

from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

from redis import Redis
rcon = Redis()

import forms, views, eventhandlers, market, testing, utils, dbase