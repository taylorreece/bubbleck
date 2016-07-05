from flask import Blueprint
from flask import flash
from flask import g
from flask import jsonify
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from bck import course
from bck import section
from bck import user
from bubbleck.helper_functions import login_required
from bubbleck.helper_functions import require_course_role
from bubbleck.forms import CourseForm
from bubbleck.forms import NewCourseForm

routes_course = Blueprint('routes_course', __name__)

# ===================================================
@routes_course.route('/course/<coursesid>/settings/addsection/')
@routes_course.route('/course/<coursesid>/settings/addsection/<section_name>')
@login_required
@require_course_role(roles=('edit','own'), json=True)
def addsection(coursesid, section_name=None):
	''' Add a section to an existing course '''
	if section_name:
		s = section.Section(name=section_name, coursesid=g.current_course.coursesid)
		s.save()
		ret = {
			'status'  : 'success',
			'message' : 'Section successfully added'
		}
	else:
		ret = {
			'status'  : 'error',
			'message' : 'No section name provided'
		}
	return jsonify(**ret)

# ===================================================
@routes_course.route('/course/<coursesid>/delete')
@login_required
@require_course_role(roles=('own',))
def delete(coursesid=None):
	''' Delete a course '''
	if request.args.get('confirm') == 'yes':
		g.current_course.deactivate()
		flash('success|%s has been deleted' % g.current_course.name)
		return redirect(url_for('routes_user.dashboard'))
	else:
		return render_template('course/delete.html')

# ===================================================
@routes_course.route('/course/new', methods=('GET','POST'))
@login_required
def new():
	''' Create a new course '''
	form = NewCourseForm(request.form)
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
@routes_course.route('/course/<coursesid>/permissions/')
@routes_course.route('/course/<coursesid>/permissions/<usersid>/<role>')
@login_required
@require_course_role(roles=('edit','own'))
def processPermissionChange(coursesid=None, usersid=None, role=None):
	''' Add or remove permissions to a user for a course '''
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
@routes_course.route('/course/<coursesid>/settings/removesection/')
@routes_course.route('/course/<coursesid>/settings/removesection/<sectionsid>')
@login_required
@require_course_role(roles=('edit','own'), json=True)
def removesection(coursesid, sectionsid=None):
	''' Deletes a section from a course, provided the user is an editor of the course '''
	ret = {}
	s = section.getSectionByID(sectionsid)
	if not s:
		ret['status'] = 'error'
		ret['message'] = 'No such section was found'
		return jsonify(**ret)
	if s.coursesid != g.current_course.coursesid:
		ret['status'] = 'error'
		ret['message'] = "The section's coursesid does not match the coursesid. What exactly are you trying to do here?"
		return jsonify(**ret)
	s.deactivate()
	ret['status'] = 'success'
	ret['message'] = 'Section successfully deactivated'
	return jsonify(**ret)

# ===================================================
@routes_course.route('/course/<coursesid>/settings/', methods=('GET','POST'))
@login_required
@require_course_role(roles=('edit','own'))
def settings(coursesid=None):
	''' Edit course settings '''
	courseform = CourseForm(request.form)
	if request.method == 'POST' and courseform.validate():
		try:
			g.current_course.name = courseform.name.data
			g.current_course.save()
			i = 0
			for section in g.current_course.getSections():
				if section.name != courseform.sections[i].data:
					section.name = courseform.sections[i].data
					section.save()
				i = i + 1
		except:
			return "An error occured while updating this course.  Please contact Taylor (taylor@reecemath.com) for details."
		flash('info|Course Updated')
	else:
		courseform.name.data = g.current_course.name
	roles = g.current_course.getUserRoles()
	users_roles = []
	for r in roles:
		users_roles.append({
				'user' : user.getUserByID(r['usersid']),
				'role' : r['role']
		})
	num_sections = 0
	for section in g.current_course.getSections():
		courseform.sections[num_sections].data = section.name
		num_sections = num_sections + 1
	return render_template('course/settings.html', users_roles=users_roles, courseform = courseform, default_num_sections=num_sections)

# ===================================================
@routes_course.route('/course/<coursesid>/view/')
@login_required
@require_course_role(roles=('view','edit','own'))
def view(coursesid=None):
	''' Default course view '''
	roles = g.current_course.getUserRoles()
	course_users = {
		'own':[user.getUserByID(key) for key,value in roles if value=='own'],
		'edit':[user.getUserByID(key) for key,value in roles if value=='edit'],
		'view':[user.getUserByID(key) for key,value in roles if value=='view']
	}
	return render_template('course/view.html', course_users=course_users)

