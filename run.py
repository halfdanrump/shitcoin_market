from app import app, socketio
from app.market.orderbook import Orderbook
from threading import Thread
# from redis import Redis
# from multiprocessing import Process


if __name__ == "__main__":
    # socketio.redis = Redis()
    book = Orderbook()
    Thread(target=book.queue_daemon).start()
    socketio.run(app, host = '127.0.0.1', port = 5000)
	# app.redis = Redis()
	# app.run(debug = True)