#!/usr/bin/python
from mat.database import mat_db

db = mat_db()

def getAllCourses():
	''' Get all course objects, return them in a list '''
	ret = []
	query = 'SELECT * FROM courses;'
	result = db.queryDictList(query)
	for r in result:
		ret.append(course(**r))
	return ret

def getCourseByID(coursesid):
	return Course.getCourseByID(Course(),coursesid)

class Course(object):
	active = None
	coursesid = None
	created_at = None
	name = None
	role = None
	updated_at = None
	
	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.active = kwargs.get('active')
		self.coursesid = kwargs.get('coursesid')
		self.created_at = kwargs.get('created_at')
		self.name = kwargs.get('name')
		self.role = kwargs.get('role')
		self.updated_at = kwargs.get('updated_at')	
		
	# ===========================================================
	def getCourseByID(self,coursesid):
		self.coursesid = coursesid
		result = db.queryOneRec('SELECT * FROM courses WHERE coursesid=%s',(self.coursesid,))
		if result:
			self.active = result['active']
			self.created_at = result['created_at']
			self.name = result['name']
			self.updated_at = result['updated_at']
			return self
		else:
			return None

	# ===========================================================
	def save(self):
		if self.coursesid:
			# It already has an ID; update it
			query = ''' UPDATE courses SET name=%s 
					WHERE coursesid=%s 
					RETURNING updated_at'''
			result = db.queryOneRec(query, (self.coursesid,))
			self.updated_at = result['updated_at'] 
		else:
			query = ''' INSERT INTO courses (name)
					VALUES (%s)
					RETURNING created_at, updated_at, coursesid, active'''
			result = db.queryOneRec(query,(self.name,))
			self.active = result['active']
			self.coursesid = result['coursesid']
			self.created_at = result['created_at']
			self.updated_at = result['updated_at']

	# ===========================================================
	def removeRoles(self,usersid):
		''' Removes all roles for a particular user for this course '''
		query = 'DELETE FROM courses_users WHERE coursesid=%s AND usersid=%s'
		db.queryNoResults(query, (self.coursesid, usersid)) 
	
	# ===========================================================
	def addOrUpdateRole(self,usersid, role):
		assert role in ('view','edit','own')
		self.removeRoles(usersid)
		query = '''INSERT INTO courses_users (coursesid, usersid, role)
				VALUES (%s,%s,%s)'''
		db.queryNoResults(query, (self.coursesid,usersid,role))
	
	# ===========================================================
	def getRole(self, usersid):
		query = 'SELECT role FROM courses_users WHERE usersid=%s AND coursesid=%s'
		return db.queryOneVal(query, (usersid, self.coursesid))

	# ===========================================================
	def getUserRoles(self):
		''' 
		Returns a list of permissions in the form [['usersid':123','role':'view'],[...]]
		'''
		query = 'SELECT usersid,role FROM courses_users WHERE coursesid=%s'
		return db.queryDictList(query,(self.coursesid,))
	
