from flask import Flask
from routes_user import routes_user

app = Flask(__name__)

app.register_blueprint(routes_user)

@app.route('/')
def index():
    return 'You have reached the MAT web interface'
