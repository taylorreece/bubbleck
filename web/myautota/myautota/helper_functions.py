from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from functools import wraps
from mat import user

# ===================================================
def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']))
		if g.current_user is None:
			flash('info|You need to log in to access ' + request.url)
			return redirect(url_for('routes_user.login', next=request.url))
		if not g.current_user.is_admin:
			flash('danger|You need to be an administrator to access this page.')
			return redirect(url_for('index'))
		return f(*args, **kwargs)
	return decorated_function

# ===================================================
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']))
		if g.current_user is None:
			flash('info|You need to log in to access ' + request.url)
			return redirect(url_for('routes_user.login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

# ===================================================
def load_user(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']))
		if g.current_user is None:
			g.current_user = user.User() # Set a blank user
		return f(*args, **kwargs)
	return decorated_function
