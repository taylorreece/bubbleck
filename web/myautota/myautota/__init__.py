from flask import Flask, render_template, request, redirect, url_for, session
from mat import user, matconfig
from helper_functions import login_required

# Import some routes that were broken out:
from routes_user import routes_user

app = Flask(__name__)

app.secret_key = matconfig.webapp_secret_key 

app.register_blueprint(routes_user)

# ===================================================
@app.route('/')
def index():
	return render_template('index.html')

