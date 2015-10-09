from flask import Blueprint
from flask import flash
from flask import g
from flask import jsonify
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from mat import course
from mat import section
from mat import user
from myautota.helper_functions import login_required
from myautota.helper_functions import require_course_access
from myautota.forms import CourseForm

routes_course = Blueprint('routes_course', __name__)

# ===================================================
@routes_course.route('/course/delete')
@routes_course.route('/course/delete/<coursesid>')
@login_required
@require_course_access
def delete(coursesid=None):
	return render_template('course/delete.html')

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
		return redirect(url_for('routes_course.view', coursesid=c.coursesid))
	return render_template('course/new.html', form=form, default_num_sections=5)

# ===================================================
@routes_course.route('/course/permissions')
@routes_course.route('/course/permissions/<coursesid>/<usersid>/<role>')
@login_required
@require_course_access
def processPermissionChange(coursesid=None, usersid=None, role=None):
	result = {}
	if role == 'remove':
		if g.current_course.getRole(usersid) == 'own':
			result['status'] = 'error'
			result['message'] = 'You cannot remove the owner of a course'
		else:
			try:
				g.current_course.removeRoles(usersid)
			except:
				result['status'] = 'error'
				result['message'] = 'Not saved... unknown error.'
				return jsonify(**result)
			result['status'] = 'success'
			result['message'] = 'Permission removed'
	elif role not in ('edit','view'):
		result['status'] = 'error'
		result['message'] = 'The role you requested (%s) is not a role.  WTF are you doing?' % role
	elif g.current_course.getRole(g.current_user.usersid) not in ('own','edit'):
		result['status'] = 'error'
		result['message'] = 'You are not the owner or editor of this course'
	elif usersid == g.current_user.usersid:
		result['status'] = 'error'
		result['message'] = 'You cannot edit your own permissions.'
	elif g.current_course.getRole(usersid) == 'own':
		result['status'] = 'error'
		result['message'] = 'You cannot change permissions for the course owner.'
	else:
		try:
			g.current_course.addOrUpdateRole(usersid,role)
		except:
			result['status'] = 'error'
			result['message'] = 'Not saved... unknown error.'
			return jsonify(**result)
		result['status'] = 'success'
		result['message'] = 'Permissions changed.'
	return jsonify(**result)

# ===================================================
@routes_course.route('/course/settings')
@routes_course.route('/course/settings/<coursesid>')
@login_required
@require_course_access
def settings(coursesid=None):
	roles = g.current_course.getUserRoles()
	users_roles = []
	for r in roles:
		users_roles.append({
				'user' : user.getUserByID(r['usersid']),
				'role' : r['role']
		})
	return render_template('course/settings.html', users_roles=users_roles)

# ===================================================
@routes_course.route('/course/view')
@routes_course.route('/course/view/<coursesid>')
@login_required
@require_course_access
def view(coursesid=None):
	return render_template('course/view.html')

