from datetime import datetime
from flask import Blueprint
from flask import flash
from flask import g
from flask import jsonify
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from mat import user
from myautota.helper_functions import anonymous_required
from myautota.helper_functions import login_required
from myautota.helper_functions import load_user 
from myautota.forms import LoginForm
from myautota.forms import RegisterForm
from myautota.forms import UserForm

routes_user = Blueprint('routes_user', __name__)

# ===================================================
@routes_user.route('/home')
@login_required
def dashboard():
	return render_template('user/dashboard.html')

# ===================================================
@routes_user.route('/ajax/userbyemail/')
@routes_user.route('/ajax/userbyemail/<email>')
@login_required
def getUsersidByEmail(email=None):
	result = {}
	if email:
		usersid = user.getUsersidByEmail(email)
		if usersid:
			result['status'] = 'success'
			result['usersid'] = usersid
		else:
			result['status'] = 'error'
			result['message'] = 'No registered user has that email address'
	else:
		result['status'] = 'error'
		result['message'] = 'You did not supply an email address'
	return jsonify(**result)

# ===================================================
@routes_user.route('/user/login', methods=('GET', 'POST'))
@anonymous_required
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		g.current_user = user.getUserByEmailAndPassword(form.email.data,form.password.data)
		if g.current_user.usersid:
			sessionid = g.current_user.createSession(ipaddress=request.remote_addr)
			session['sessionid'] = sessionid
			return redirect(url_for('routes_user.dashboard'))
		else:
			flash('danger|Login Incorrect')
	return render_template('user/login.html', form=form)

# ===================================================
@routes_user.route('/user/logout')
@login_required
def logout():
	g.current_user = None
	user.deleteSession(session['sessionid'])
	flash('info|You have been logged out.')
	return redirect(url_for('routes_user.login')) 

# ===================================================
@routes_user.route('/user/register', methods=('GET', 'POST'))
@anonymous_required
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			u = user.User( 
				email              = form.email.data,
			 	name               = form.name.data,
				password_plaintext = form.password.data,
				teachername        = form.teachername.data,
			)
			u.save()
		except:
			return "An error occured while creating your account.  Please contact taylor (taylor@reecemath.com) for details"
		flash('info|A user account for %s has been created.  Please log in.' % form.email.data)
	
		return redirect(url_for('routes_user.login'))
	oauthProviders = {	
		'facebook'    : 'Facebook',
		'google-plus' : 'Google',
		'twitter'     : 'Twitter'	
	}
	return render_template('user/register.html', form=form, oauthProviders=oauthProviders)

# ===================================================
@routes_user.route('/user/closesession/')
@routes_user.route('/user/closesession/<sessionid>')
@login_required
def closesession(sessionid=None):
	ret = {}
	result = g.current_user.closeSession(sessionid)
	if result:
		ret['status'] = 'success'
		ret['message'] = 'Session successfully closed'
	else:
		ret['status'] = 'error'
		ret['message'] = 'Cannot close this session'
	return jsonify(**ret)

# ===================================================
@routes_user.route('/user/settings', methods=('GET', 'POST'))
@login_required
def settings():
	form = UserForm(request.form)
	if request.method == 'POST':
		if form.validate():
			try:
				g.current_user.email       = form.email.data
				g.current_user.name        = form.name.data
				g.current_user.teachername = form.teachername.data
				g.current_user.save()
			except:
				return "An error occured while updating your account.  Please contact taylor (taylor@reecemath.com) for details."
			flash('info|Account Updated')
	else:
		form.email.data       = g.current_user.email
		form.name.data        = g.current_user.name
		form.teachername.data = g.current_user.teachername
	return render_template('user/settings.html', form=form, current_session=session['sessionid'], now=datetime.now())

