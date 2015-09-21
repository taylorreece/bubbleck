from flask import Blueprint, request, render_template
from mat import user
from helper_functions import login_required
from forms import LoginForm

routes_user = Blueprint('routes_user', __name__)

@routes_user.route("/login")
def login():
	form = LoginForm()
	return render_template('login.html', form=form)
