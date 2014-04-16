from flask import Flask

app = Flask(__name__)

from app import config
app.config.from_object(config.app_config)

from flask.ext.socketio import SocketIO
socketio = SocketIO(app)

from app import views
#from app import market