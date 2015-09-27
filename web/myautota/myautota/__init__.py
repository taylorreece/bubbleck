from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from myautota.helper_functions import login_required
from myautota.helper_functions import load_user
from mat import matconfig
from mat import user

# Import some routes that were broken out:
from myautota.routes_admin import routes_admin
from myautota.routes_user import routes_user

# Set up the app
app = Flask(__name__)
app.secret_key = matconfig.webapp_secret_key 
app.register_blueprint(routes_admin)
app.register_blueprint(routes_user)

# For recaptcha
app.config['RECAPTCHA_PUBLIC_KEY'] = matconfig.recaptcha_public_key
app.config['RECAPTCHA_PRIVATE_KEY'] = matconfig.recaptcha_private_key

# ===================================================
@app.route('/')
@load_user
def index():
	return render_template('index.html')

# ===================================================
@app.route('/about')
@load_user
def about():
	return render_template('about.html')

# ===================================================
@app.route('/contact')
@load_user
def contact():
	return render_template('contact.html')

