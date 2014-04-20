from app import app, socketio
# from redis import Redis



if __name__ == "__main__":
    # socketio.redis = Redis()
    socketio.run(app, host = '127.0.0.1', port = 5000)
	# app.redis = Redis()
	# app.run(debug = True)