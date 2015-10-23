from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from myautota.helper_functions import login_required
from myautota.helper_functions import require_course_role

routes_exam = Blueprint('routes_exam', __name__)

# ===================================================
@routes_exam.route('/new')
@login_required
def new():
	return "New Exam"
	#return render_template('exam/new.html')

# ===================================================
@routes_exam.route('/view/<coursesid>/<examsid>')
@login_required
@require_course_role(roles=('view','edit','own'))
def view(coursesid,examsid):
	return "Viewing exam %s" % examsid
	#return render_template('exam/view.html')

