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
from bck import user
from bubbleck.helper_functions import anonymous_required
from bubbleck.helper_functions import login_required
from bubbleck.helper_functions import load_user 
from bubbleck.helper_functions import queueEmail
from bubbleck.forms import ChangePasswordForm
from bubbleck.forms import ForgottenPasswordForm
from bubbleck.forms import LoginForm
from bubbleck.forms import RegisterForm
from bubbleck.forms import UserForm

routes_user = Blueprint('routes_user', __name__)

# ===================================================
@routes_user.route('/user/settings/changepassword', methods=('GET','POST'))
@login_required
def changepassword():
	''' Change a users password '''
	result = {}
	form = ChangePasswordForm(request.form)
	if form.validate():
		if g.current_user.checkPassword(form.oldpassword.data):
			g.current_user.setPassword(form.newpassword.data)
			g.current_user.save()
			result['status'] = 'success'
			flash('success|Password changed successfully')
			# TODO: email a notice that their password changed.
		else:
			result['status'] = 'error'
			result['message'] = 'The current password you supplied is incorrect.'
	else:
		result['status'] = 'error'
		result['message'] = 'Validation failed with the following errors: %s' % form.errors
	return jsonify(**result)

# ===================================================
@routes_user.route('/user/closesession/')
@routes_user.route('/user/closesession/<sessionid>')
@login_required
def closesession(sessionid=None):
	''' User can close an open session (not the current session, but another one) '''
	result = {}
	if g.current_user.closeSession(sessionid):
		result['status'] = 'success'
		result['message'] = 'Session successfully closed'
	else:
		result['status'] = 'error'
		result['message'] = 'Cannot close this session'
	return jsonify(**result)

# ===================================================
@routes_user.route('/user/settings/deactivate', methods=('GET','POST'))
@login_required
def deactivate():
	''' Deactivate an account '''
	if request.args.get('confirm') == 'yes':
		g.current_user.deactivate()
		flash('success|Your account has been deactivated')
		return redirect(url_for('index'))
	else:
		return render_template('user/deactivate.html')

# ===================================================
@routes_user.route('/home')
@login_required
def dashboard():
	''' Default user dashboard '''
	return render_template('user/dashboard.html')

# ===================================================
@routes_user.route('/user/forgot', methods=('GET','POST'))
@anonymous_required
def forgot():
	''' Forgot my password dialogue '''
	form = ForgottenPasswordForm(request.form)
	if request.method == 'POST' and form.validate():
		email = form.email.data,
		usersid = user.getUsersidByEmail(email)
		if usersid:
			u = user.getUserByID(usersid)
			reset_key = u.generatePasswordResetKey()
			queueEmail(
				usersid = usersid,
				subject = 'BubbleCK Password Reset',
				body = '''
Dear %s,
	You, or someone pretending to be you, has requested that your password for bubbleck.com be reset.  If you did not make this request, ignore this email.  Everything is fine.  If you did make this request, please visit %s%s to reset your password.
	Cheers,
		Taylor
					''' % (u.teachername, request.url_root[:-1], url_for('routes_user.passwordreset',reset_key=reset_key)),
				show_as_web_msg = False
			)
			flash('success|An email with instructions on how to reset your password has been sent to %s.' % email)
			return redirect(url_for('index'))
		else:
			flash('danger|No user is registered under email address (%s)' % email)
			return render_template('user/forgot.html', form=form)
	else:
		return render_template('user/forgot.html', form=form)

# ===================================================
@routes_user.route('/ajax/userbyemail/')
@routes_user.route('/ajax/userbyemail/<email>')
@login_required
def getUsersidByEmail(email=None):
	''' Get a userid by email ; called out by the client '''
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
	''' Login dialogue '''
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
	''' Logout dialogue '''
	g.current_user.closeSession(session['sessionid'])
	g.current_user = None
	flash('info|You have been logged out.')
	return redirect(url_for('routes_user.login')) 

# ===================================================
@routes_user.route('/user/reset/<reset_key>', methods=('GET', 'POST'))
@load_user
def passwordreset(reset_key):
	''' Password reset dialogue '''
	form = ChangePasswordForm(request.form)	
	u = user.getUserByResetKey(reset_key)
	if u:
		if request.method == 'POST' and form.validate():
			new_password = form.newpassword.data
			u.setPassword(form.newpassword.data)
			u.save()
			flash('success|Password reset successfully')
			return redirect(url_for('routes_user.login'))
		else:
			return render_template('user/passwordreset.html', form=form, reset_key=reset_key)
	else:
		flash('error|This password rest key is invalid')
		return redirect(url_for('index')) 


# ===================================================
@routes_user.route('/user/register', methods=('GET', 'POST'))
@anonymous_required
def register():
	''' Register form '''
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
	oauth_providers = {	
		'facebook'    : 'Facebook',
		'google-plus' : 'Google',
		'twitter'     : 'Twitter'	
	}
	return render_template('user/register.html', form=form, oauth_providers=oauth_providers)

# ===================================================
@routes_user.route('/user/settings', methods=('GET', 'POST'))
@login_required
def settings():
	''' User settings form '''
	userform = UserForm(request.form)
	if request.method == 'POST' and userform.validate():
		try:
			g.current_user.email       = userform.email.data
			g.current_user.name        = userform.name.data
			g.current_user.teachername = userform.teachername.data
			g.current_user.save()
		except:
			return "An error occured while updating your account.  Please contact taylor (taylor@reecemath.com) for details."
		flash('info|Account Updated')
	else:
		userform.email.data       = g.current_user.email
		userform.name.data        = g.current_user.name
		userform.teachername.data = g.current_user.teachername
	subscription = g.current_user.getSubscriptionExpiration()
	if subscription:
		subscription['expiration'] = datetime.strftime(subscription['expiration'],'%B %d, %Y')
	return render_template('user/settings.html', 
				changepasswordform = ChangePasswordForm(), 
				current_session=session['sessionid'], 
				now=datetime.now(),
				subscription=subscription,
				userform=userform
				)

# ===================================================
@routes_user.route('/user/settings/subscribe')
@login_required
def subscribe():
	''' Users can subscribe to the site, paying money for disabling of ads, access to mobile app '''
	# TODO: Create a subscription page, tie in to paypal, etc.
	return "not yet implemented"

