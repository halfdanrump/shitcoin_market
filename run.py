from app import flapp, socketio
from app.market.orderbook import Orderbook
from threading import Thread
# from redis import Redis
# from multiprocessing import Process

import argparse
if __name__ == "__main__":
    # socketio.redis = Redis()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--env', required=True, choices('test', 'dev', 'prod'))
    # args = parser.parse_args()

    # if args.env == 'test':
    #     flapp.config.from_object('app.config.app_config.TestConfig)

    book = Orderbook()
    flapp.book = book
    flapp.orderbooks[book.ID] = book
    Thread(target=book.queue_daemon).start()
    socketio.run(flapp, host = '127.0.0.1', port = 5000)
	# app.redis = Redis()
	# app.run(debug = True)