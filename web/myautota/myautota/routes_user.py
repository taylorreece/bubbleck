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
#from forms import LoginForm
#from forms import RegisterForm

routes_user = Blueprint('routes_user', __name__)

# ===================================================
@routes_user.route('/user')
@load_user
def dashboard():
#	form = LoginForm()
	return render_template('user/dashboard.html')#, form=form)


# ===================================================
@routes_user.route('/user/login')
@load_user
def login():
	return render_template('user/login.html')

# ===================================================
@routes_user.route('/user/logout')
@login_required
def logout():
	g.current_user = None
	user.deleteSession(session['sessionid'])
	flash('You have been logged out.')
	return redirect(url_for('routes_user.login')) 

# ===================================================
@routes_user.route('/user/register')
@load_user
def register():
	return render_template('user/register.html')

# ===================================================
@routes_user.route('/user/settings')
@load_user
def settings():
	return render_template('user/settings.html')

