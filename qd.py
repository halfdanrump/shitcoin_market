#!/usr/bin/env python
from app import app
from app.market.orderbook import queue_daemon
queue_daemon(app)