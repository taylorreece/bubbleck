from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from myautota.helper_functions import admin_required
from myautota.helper_functions import login_required
from myautota.helper_functions import load_user

routes_admin = Blueprint('routes_admin', __name__)

# ===================================================
@routes_admin.route('/admin')
@admin_required
def dashboard():
	return render_template('admin/dashboard.html')

