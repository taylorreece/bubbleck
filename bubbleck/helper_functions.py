from flask import flash
from flask import g
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from functools import wraps
from bck import course
from bck import database
from bck import exam
from bck import user

# ===================================================
def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']),request.remote_addr)
		if g.current_user is None:
			flash('info|You need to log in to access ' + request.url)
			return redirect(url_for('routes_user.login', next=request.url))
		if not g.current_user.is_admin:
			flash('danger|You need to be an administrator to access this page.')
			return redirect(url_for('index'))
		g.current_user.logged_in = True
		return f(*args, **kwargs)
	return decorated_function

# ===================================================
def anonymous_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']),request.remote_addr)
		if g.current_user is not None:
			return redirect(url_for('routes_user.dashboard'))
		g.current_user = user.User()
		return f(*args, **kwargs)
	return decorated_function

# ===================================================
def load_exam(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			e = exam.getExamByID(kwargs['examsid'])
		except KeyError:
			flash('warning|No exam key was specified.')
			return redirect(url_for('routes_user.dashboard'))
		if not e:
			flash('warning|Exam not found.')
			return redirect(url_for('routes_user.dashboard'))
		if e.coursesid != int(kwargs['coursesid']):
			flash('warning|The courses id does not match the exams id.')
			return redirect(url_for('routes_user.dashboard'))
		g.current_exam = e	# Some stuff
		return f(*args, **kwargs)
	return decorated_function

# ===================================================
def load_user(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']),request.remote_addr)
		if g.current_user is None:
			g.current_user = user.User() # Set a blank user
		else:
			g.current_user.logged_in = True
		return f(*args, **kwargs)
	return decorated_function
	
# ===================================================
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		g.current_user = None
		if 'sessionid' in session: 
			g.current_user = user.getUserBySessionID(str(session['sessionid']),request.remote_addr)
		if g.current_user is None:
			flash('info|You need to log in to access ' + request.url)
			return redirect(url_for('routes_user.login', next=request.url))
		g.current_user.logged_in = True
		return f(*args, **kwargs)
	return decorated_function

# ===================================================
def require_course_role(roles, json=False):
	def decorator(method):
		@wraps(method)
		def f(*args, **kwargs):	
			if json:
				jsonret = {}
			try:
				c = course.getCourseByID(kwargs['coursesid'])
			except KeyError:
				if json:
					jsonret['status'] = 'error'
					jsonret['message'] = 'Course not found'
					return jsonify(**jsonret)	
				flash('warning|The requested course was not found.')	
				return redirect(url_for('routes_user.dashboard'))	
			if c:
				role = c.getRole(g.current_user.usersid)
				if g.current_user.is_admin:
					role = 'own'
				if role is None or role not in roles:
					if json:
						jsonret['status'] = 'error'
						jsonret['message'] = 'You do not have permission to make this change'
						return jsonify(**jsonret)
					flash('warning|You do not have permission to access that course.  You have role "{0}", but require "{1}".'.format((role,'" or "'.join(roles))))
					return redirect(url_for('routes_user.dashboard'))	
			else:
				if json:
					jsonret['status'] = 'error'
					jsonret['message'] = 'Course not found'
					return jsonify(**jsonret)
				flash('warning|The requested course was not found.')	
				return redirect(url_for('routes_user.dashboard'))	
			g.current_course = c
			return method(*args, **kwargs)
		return f
	return decorator

# ===================================================
def queueEmail(usersid=None, additional_to=None, additional_cc=None, additional_bcc=None, subject=None, body=None, show_as_web_msg=True):
	db = database.BckDB()	
	db.queryNoResults('''INSERT INTO email_users (usersid, additional_to, additional_cc, additional_bcc, subject, body, show_as_web_msg) 
				VALUES (%s,%s,%s,%s,%s,%s,%s)''',
			(usersid, additional_to, additional_cc, additional_bcc, subject, body, show_as_web_msg))	
	
