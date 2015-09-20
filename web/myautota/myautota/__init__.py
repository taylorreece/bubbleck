from flask import Flask, render_template
from functools import wraps

# Import some routes that were broken out:
from routes_user import routes_user

app = Flask(__name__)

app.register_blueprint(routes_user)

# ===================================================
@app.route('/')
def index():
    return render_template('index.html')

# ===================================================
# TODO: make sure this actually works; set up a login interface
# test the crap out of this wrapper business.
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None:
			return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function
