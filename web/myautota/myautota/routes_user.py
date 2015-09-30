from flask import Blueprint
from flask import flash
from flask import g
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

routes_user = Blueprint('routes_user', __name__)

# ===================================================
@routes_user.route('/user')
@load_user
def dashboard():
	return render_template('user/dashboard.html')#, form=form)


# ===================================================
@routes_user.route('/user/login', methods=('GET', 'POST'))
@anonymous_required
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		g.current_user = user.getUserByEmailAndPassword(form.email.data,form.password.data)
		if g.current_user.usersid:
			sessionid = g.current_user.createSession()
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
			u = user.User( email = form.email.data,
				  name = form.name.data,
				  password_plaintext = form.password.data,
				  teachername = form.teachername.data,
			)
			u.save()
		except:
			return "An error occured while creating your account.  Please contact taylor (taylor@reecemath.com) for details"
		flash('info|A user account for %s has been created.  Please log in.' % form.email.data)
		return redirect(url_for('routes_user.login'))
	return render_template('user/register.html',form=form)

# ===================================================
@routes_user.route('/user/settings')
@load_user
def settings():
	return render_template('user/settings.html')

