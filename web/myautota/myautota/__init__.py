from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from helper_functions import login_required
from mat import matconfig
from mat import user

# Import some routes that were broken out:
from routes_user import routes_user

# Set up the app
app = Flask(__name__)
ctx = app.app_context()
ctx.push()
app.secret_key = matconfig.webapp_secret_key 
app.register_blueprint(routes_user)

g.current_user = None

# ===================================================
@app.route('/')
def index():
	return render_template('index.html')

# ===================================================
@app.route('/about')
def about():
	return render_template('about.html')

