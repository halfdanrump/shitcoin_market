import logging.config, logging.handlers, yaml
from config.app_config import basedir
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
handler = logging.handlers.RotatingFileHandler('orderbook.log', maxBytes = 10**6)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamhandler = logging.StreamHandler(sys.stdout)
streamhandler.setFormatter(formatter)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(streamhandler)

logger.info('\n\n#################Starting server!#################\n')



from flask import Flask
flapp = Flask(__name__)

from app.lib.flask_bootstrap import Bootstrap
Bootstrap(flapp)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(flapp)


from flask.ext.openid import OpenID
print basedir
oid = OpenID(flapp, os.path.join(basedir, 'tmp'), safe_roots=[])

from app.config.app_config import DevelopmentConfig
flapp.config.from_object(DevelopmentConfig())

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(flapp)


flapp.orderbooks = dict()

from flask.ext.socketio import SocketIO
socketio = SocketIO(flapp)

from redis import Redis
rcon = Redis()



import views, forms
# import forms, views, eventhandlers, market, testing, utils, dbase