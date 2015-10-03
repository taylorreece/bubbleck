from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from mat import course
from mat import section
from myautota.helper_functions import login_required
from myautota.forms import CourseForm

routes_course = Blueprint('routes_course', __name__)

# ===================================================
@routes_course.route('/course/new', methods=('GET','POST'))
@login_required
def new():
	form = CourseForm(request.form)
	if request.method == 'POST' and form.validate():
		c = course.Course(name=form.name.data)
		c.save()
		c.addOrUpdateRole(g.current_user.usersid, 'own')
		num_sections = 0
		for section_name in form.sections.data:
			if section_name:
				num_sections = num_sections + 1
				s = section.Section(name=section_name, coursesid=c.coursesid)
				s.save()
		flash('success|Course %s was created with %s sections.' % (c.name,num_sections))
		return redirect(url_for('routes_user.dashboard'))
	return render_template('course/new.html', form=form)

