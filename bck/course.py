#!/usr/bin/python3
from bck import exam, section
from bck.database import BckDB
from bck.bckobject import BckObject
db = BckDB()

def getAllCourses():
	''' Get all course objects, return them in a list '''
	ret = []
	query = 'SELECT * FROM courses;'
	result = db.query_dict_list(query)
	for r in result:
		ret.append(course(**r))
	return ret

def getCourseByID(coursesid):
	return Course.getCourseByID(Course(),coursesid)

class Course(BckObject):
	''' An object representation of a course instance '''
	active = True
	coursesid = None
	created_at = None
	name = None
	updated_at = None
	
	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.set_attributes(kwargs)

	# ===========================================================
	def addOrUpdateRole(self,usersid, role):
		''' Takes a usersid and role, and adds that role to this course instance '''
		assert role in ('view','edit','own')
		self.removeRoles(usersid)
		query = '''INSERT INTO courses_users (coursesid, usersid, role)
				VALUES (%s,%s,%s)'''
		db.query_no_results(query, (self.coursesid,usersid,role))
		
	# ===========================================================
	def getCourseByID(self,coursesid):
		''' Returns the course that matches provided id number '''
		self.coursesid = coursesid
		result = db.query_one_rec('SELECT * FROM courses WHERE coursesid=%s',(self.coursesid,))
		if result:
			self.set_attributes(result)
			return self
		else:
			return None

	# ===========================================================
	def getExams(self):
		''' Returns a list of exams associated with this course instance '''
		ret = []
		query = 'SELECT * FROM exams WHERE coursesid=%s AND active'
		exams = db.query_dict_list(query,(self.coursesid,))
		for e in exams:
			ret.append(exam.Exam(**e))
		return ret
	
	# ===========================================================
	def getRole(self, usersid):
		query = 'SELECT role FROM courses_users WHERE usersid=%s AND coursesid=%s'
		return db.query_one_val(query, (usersid, self.coursesid))

	# ===========================================================
	def getSections(self):
		''' Returns a list of sections associated with this course instance '''
		ret = []
		query = 'SELECT * FROM sections WHERE coursesid=%s AND active ORDER BY sectionsid'
		sections = db.query_dict_list(query,(self.coursesid,))
		for e in sections:
			ret.append(section.Section(**e))
		return ret

	# ===========================================================
	def getUserRoles(self):
		''' 
		Returns a list of permissions in the form [['usersid':'123','role':'view'],[...]]
		'''
		query = "SELECT usersid,role FROM courses_users WHERE coursesid=%s ORDER BY role='view', role='edit', role='own'"
		return db.query_dict_list(query,(self.coursesid,))

	# ===========================================================
	def removeRoles(self,usersid):
		''' Removes all roles for a particular user for this course '''
		query = 'DELETE FROM courses_users WHERE coursesid=%s AND usersid=%s'
		db.query_no_results(query, (self.coursesid, usersid)) 
	
	# ===========================================================
	def save(self):
		if self.coursesid:
			# It already has an ID; update it
			query = ''' UPDATE courses SET name=%s, active=%s
					WHERE coursesid=%s 
					RETURNING updated_at'''
			result = db.query_one_rec(query, (self.name, self.active, self.coursesid))
			self.set_attributes(result)
		else:
			query = ''' INSERT INTO courses (name)
					VALUES (%s)
					RETURNING created_at, updated_at, coursesid, active'''
			result = db.query_one_rec(query,(self.name,))
			self.set_attributes(result)

	# ===========================================================
	def deactivate(self):
		query = 'UPDATE courses SET active=false WHERE coursesid=%s'
		return db.query_no_results(query, (self.coursesid,))

