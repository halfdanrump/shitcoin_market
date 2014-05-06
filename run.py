from app import flapp, socketio, logger
from app.market.orderbook import Orderbook
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
        flapp.config.from_object('app.config.app_config.TestConfig')
    elif args.env == 'dev':
        flapp.config.from_object('app.config.app_config.DevelopmentConfig')
    elif args.env == 'prod':
        flapp.config.from_object('app.config.app_config.DevelopmentConfig')
    
    book = Orderbook()
    flapp.book = book
    flapp.orderbooks[book.ID] = book
    Thread(target=book.queue_daemon).start()
    socketio.run(flapp, host = '127.0.0.1', port = 5000)
	# app.redis = Redis()
	# app.run(debug = True)