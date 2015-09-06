from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'You have reached the MAT web interface'
