from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from mat import user
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
@routes_user.route('/user/login')
@load_user
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		return 'Authenticated'
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
@load_user
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		# TODO: use the data from this form to create an actual user
		return "Got it!"
	return render_template('user/register.html',form=form)

# ===================================================
@routes_user.route('/user/settings')
@load_user
def settings():
	return render_template('user/settings.html')

