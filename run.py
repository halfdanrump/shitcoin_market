from app import flapp, socketio, logger, db
from app.market.orderbook import Orderbook
from app.config.app_config import TestConfig, DevelopmentConfig, ProductionConfig
from threading import Thread
# from redis import Redis
# from multiprocessing import Process

import argparse
if __name__ == "__main__":
    # socketio.redis = Redis()
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', choices = ('test', 'dev', 'prod'), default = 'dev')
    args = parser.parse_args()

    logger.info('Starting Flask app in %s environment'%args.env)

    if args.env == 'test':
        configuration = TestConfig()
    elif args.env == 'dev':
        configuration = DevelopmentConfig()
    elif args.env == 'prod':
        configuration = ProductionConfig()
    
    flapp.config.from_object(configuration)

    # print flapp.config    
    book = Orderbook()
    flapp.book = book
    flapp.orderbooks[book.uuid] = book
    Thread(target=book.queue_daemon).start()
    socketio.run(flapp, host = '127.0.0.1', port = 5000)
	# app.redis = Redis()
	# app.run(debug = True)