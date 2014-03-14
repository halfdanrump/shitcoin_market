from app import app
from app.market.utils import queue_daemon
if __name__ == "__main__":
    app.run(debug = True)
    queue_daemon(app)
