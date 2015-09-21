from flask import redirect, request, session, url_for 
from mat import user
from functools import wraps

# ===================================================
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		global current_user
		current_user = None
		if 'sessionid' in session: 
			sessionid = session['sessionid']
			print "Sessionid: " , sessionid
			current_user = user.getUserBySessionID(sessionid)
		if current_user is None:
			return redirect(url_for('routes_user.login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

