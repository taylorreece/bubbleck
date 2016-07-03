# ===================================================
# Before anything, make sure the web service is running
# against the correct schema version.
schema_version = 1
from bck import database
try:
	if schema_version != int(database.BckDB().getSchemaVersion()):
		exit('Schema version of the database is incorrect.  Expecting %s, but got %s' % (schema_version,database.BckDB().getSchemaVersion()))
except TypeError:
	exit('Could not identify schema version.')

# ===================================================
from datetime import timedelta
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from bubbleck.helper_functions import anonymous_required
from bubbleck.helper_functions import login_required
from bubbleck.helper_functions import load_user
from bck import bckconfig
from bck import user

# Import some routes that were broken out:
from bubbleck.routes_admin import routes_admin
from bubbleck.routes_course import routes_course
from bubbleck.routes_exam import routes_exam
from bubbleck.routes_user import routes_user

# Set up the app
app = Flask(__name__)
app.secret_key = bckconfig.webapp_secret_key 
app.register_blueprint(routes_admin)
app.register_blueprint(routes_course)
app.register_blueprint(routes_exam)
app.register_blueprint(routes_user)

# For recaptcha
app.config['RECAPTCHA_PUBLIC_KEY'] = bckconfig.recaptcha_public_key
app.config['RECAPTCHA_PRIVATE_KEY'] = bckconfig.recaptcha_private_key


# ===================================================
@app.before_request
def beforerequest():
	g.sitename = '&#x24b7;U&#x24b7;&#x24b7;L&#x24ba;&#x2714;'
	session.permanent = True
	app.permanent_session_lifetime = timedelta(days=365)

# ===================================================
@app.route('/')
@anonymous_required
def index():
	return render_template('marketing/index.html')

# ===================================================
@app.route('/about')
@load_user
def about():
	return render_template('marketing/about.html')

# ===================================================
@app.route('/contact')
@load_user
def contact():
	return render_template('marketing/contact.html')

# ===================================================
@app.route('/about/mobile')
@load_user
def aboutMobile():
	return render_template('marketing/mobile.html')

