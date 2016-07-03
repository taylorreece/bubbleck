from bubbleck import app

@app.route('/')
def index():
	return 'Hello World!'

@app.route('/test')
def test():
	return 'This is a test'
