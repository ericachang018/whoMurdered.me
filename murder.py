from model.database import db_session

@app.teardown_request
	def shutdown_session(exception = None)
		db_session.remove()