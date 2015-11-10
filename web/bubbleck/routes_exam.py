from flask import Blueprint
from flask import flash
from flask import g
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from bck import exam

from bubbleck.helper_functions import load_exam
from bubbleck.helper_functions import login_required
from bubbleck.helper_functions import require_course_role

from reportlab.pdfgen import canvas

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
@routes_exam.route('/exam/new/<coursesid>', methods=('GET','POST'))
@login_required
@require_course_role(roles=('edit','own'))
def new(coursesid):
	if request.method == 'POST':
		try:
			e = exam.Exam()
			e.coursesid		= coursesid
			e.layout 		= request.form['layout']
			e.name			= request.form['name']
			e.show_coursename 	= request.form['show_coursename']
			e.show_directions 	= request.form['show_directions']
			e.show_points 		= request.form['show_points']
			e.show_teachername 	= request.form['show_teachername']
			e.save()
		except Exception as err:
			print(err)
			ret = {
				'status'  : 'error',
				'message' : 'There was an error parsing your input.  You really shouldn\'t see this error.  Please contact Taylor (taylor@reecemath.com), taking note of what you were doing that resulted in this error.'
			}
			return jsonify(**ret)
		ret = {
			'status'  : 'success',
			'examsid' : e.examsid,
		}
		return jsonify(**ret)
	exam_format_import = []
	for c in g.current_user.getCourses():
		for e in c.getExams():
			exam_format_import.append({ 'course_name' : c.name, 'exam_layout' : e.layout, 'exam_name' : e.name})	
	return render_template('exam/new.html', exam_format_import = exam_format_import)

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/pdf')
@login_required
@require_course_role(roles=('view','edit','own'))
@load_exam
def pdf(coursesid,examsid):
	# TODO: Obviously fix this up to generate actual PDFs; this is just a proof of concept
	from io import BytesIO
	output = BytesIO()

	p = canvas.Canvas(output)
	p.drawString(100, 100, 'Hello')
	p.showPage()
	p.save()

	pdf_out = output.getvalue()
	output.close()

	response = make_response(pdf_out)
	response.headers['Content-Disposition'] = "filename='sakulaci.pdf"
	response.mimetype = 'application/pdf'

	return response

# ===================================================
@routes_exam.route('/exam/view/<coursesid>/')
@routes_exam.route('/exam/view/<coursesid>/<examsid>')
@login_required
@require_course_role(roles=('view','edit','own'))
@load_exam
def view(coursesid,examsid=''):
	return render_template('exam/view.html')

# ===================================================
@routes_exam.route('/exam/<coursesid>/<examsid>/share')
@login_required
@require_course_role(roles=('edit','own'))
@load_exam
def share(coursesid,examsid):
	return "Sharing exam %s" % examsid
	#return render_template('exam/share.html')

