from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from functools import wraps
from mat import user

# ===================================================
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(session['sessionid'])
		if g.current_user is None:
			flash('You need to log in to access (request.url)')
			return redirect(url_for('routes_user.login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

