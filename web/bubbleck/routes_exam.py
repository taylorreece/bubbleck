from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from bubbleck.helper_functions import load_exam
from bubbleck.helper_functions import login_required
from bubbleck.helper_functions import require_course_role

routes_exam = Blueprint('routes_exam', __name__)

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/delete')
@login_required
@require_course_role(roles=('edit','own'))
@load_exam
def delete(coursesid,examsid):
	if request.args.get('confirm') == 'yes':
		g.current_exam.deactivate()
		flash('success|%s has been deleted' % g.current_exam.name)
		return redirect(url_for('routes_user.dashboard'))
	else:
		return render_template('exam/delete.html')

# ===================================================
@routes_exam.route('/exam/new/<coursesid>')
@login_required
@require_course_role(roles=('edit','own'))
def new(coursesid):
	return render_template('exam/new.html')

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/pdf')
@login_required
@require_course_role(roles=('view','edit','own'))
@load_exam
def pdf(coursesid,examsid):
	return "Viewing PDF of %s" % examsid

# ===================================================
@routes_exam.route('/view/<coursesid>/<examsid>')
@login_required
@require_course_role(roles=('view','edit','own'))
@load_exam
def view(coursesid,examsid):
	return render_template('exam/view.html')

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/share')
@login_required
@require_course_role(roles=('edit','own'))
@load_exam
def share(coursesid,examsid):
	return "Sharing exam %s" % examsid
	#return render_template('exam/share.html')


