
from app import logger, db
import models

def init_db(flask_app):
	logger.info('Initializing database with URI %s'%flask_app.config['SQLALCHEMY_DATABASE_URI'])
	db.init_app(flask_app)
	db.drop_all()
	db.create_all()

