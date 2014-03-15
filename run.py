from app import app
from app.market.orderbook import queue_daemon
if __name__ == "__main__":
    #queue_daemon(app)
    app.run(debug = True)

