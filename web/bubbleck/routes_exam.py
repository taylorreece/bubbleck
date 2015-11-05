from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from bubbleck.helper_functions import login_required
from bubbleck.helper_functions import require_course_role

routes_exam = Blueprint('routes_exam', __name__)

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/delete')
@login_required
@require_course_role(roles=('edit','own'))
def delete(coursesid,examsid):
	return "Deleting exam %s" % examsid
	#return render_template('exam/view.html')

# ===================================================
@routes_exam.route('/exam/new/<coursesid>')
@login_required
@require_course_role(roles=('edit','own'))
def new(coursesid):
	return "New Exam"
	#return render_template('exam/new.html')

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/pdf')
@login_required
@require_course_role(roles=('view','edit','own'))
def pdf(coursesid,examsid):
	return "Viewing exam %s" % examsid
	#return render_template('exam/view.html')

# ===================================================
@routes_exam.route('/view/<coursesid>/<examsid>')
@login_required
@require_course_role(roles=('view','edit','own'))
def view(coursesid,examsid):
	return "Viewing exam %s" % examsid
	#return render_template('exam/view.html')

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/share')
@login_required
@require_course_role(roles=('edit','own'))
def share(coursesid,examsid):
	return "Sharing exam %s" % examsid
	#return render_template('exam/view.html')


