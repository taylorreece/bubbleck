from flask import Flask, render_template
from routes_user import routes_user

app = Flask(__name__)

app.register_blueprint(routes_user)

@app.route('/')
def index():
    return render_template('index.html')
