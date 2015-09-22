from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from mat import user
from helper_functions import login_required
from forms import LoginForm
from forms import RegisterForm

routes_user = Blueprint('routes_user', __name__)

# ===================================================
@routes_user.route("/login")
def login():
	form = LoginForm()
	return render_template('login.html', form=form)

# ===================================================
@routes_user.route('/register')
def register():
	form = RegisterForm()
	return render_template('register.html', form=form)

# ===================================================
@routes_user.route('/logout')
@login_required
def logout():
	g.current_user = None
	user.deleteSession(session['sessionid'])
	flash('You have been logged out.')
	return redirect(url_for('routes_user.login')) 

