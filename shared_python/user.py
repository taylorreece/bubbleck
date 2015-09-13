#!/usr/bin/python
from mat.database import mat_db
from mat import course
from mat import matconfig

db = mat_db()


def getUsers():
	''' Get all users '''
	return getUsersByID()

def getUsersByID(usersids=None):
	''' Get multiple user objects, return them in a list '''
	ret = []
	if usersids:
		query = 'SELECT * FROM users WHERE usersid IN %s'
		result = db.queryDictList(query, (usersids,))
	else: 
		query = 'SELECT * FROM users'
		result = db.queryDictList(query)
	for r in result:
		ret.append(User(**r))
	return ret

def getUserByID(usersid):
	return User.getUserByID(User(),usersid)

class User(object):
	created_at = None
	email = None
	name = None
	password = None
	password_plaintext = None
	teachername = None
	updated_at = None
	usersid = None

	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.created_at = kwargs.get('created_at')
		self.email = kwargs.get('email')
		self.name = kwargs.get('name')
		self.password = kwargs.get('password')
		self.password_plaintext = kwargs.get('password_plaintext')
		self.teachername = kwargs.get('teachername')
		self.updated_at = kwargs.get('updated_at')
		self.usersid = kwargs.get('usersid')
		
	# ===========================================================
	def getUserByID(self,usersid):
		self.usersid = usersid
		result = db.queryOneRec('SELECT * FROM users WHERE usersid=%s',(self.usersid,))
		if result:
			self.created_at = result['created_at']
			self.email = result['email']
			self.name = result['name']
			self.password = result['password']
			self.teachername = result['teachername']
			self.updated_at = result['updated_at']
			return self
		else:
			return None

	# ===========================================================
	def save(self):
		if self.usersid:
			# A user already exists; we're updating it.
			if password_plaintext:
				result = db.queryOneRec(
						'''UPDATE users SET email=%s, name=%s, teachername=%s, password=MD5(%s)
							WHERE usersid=%s
							RETURNING updated_at, password''',
						(self.email, 
						 self.name, 
						 self.teachername, 
						 self.password_plaintext + matconfig.password_salt, 
						 self.usersid)
					)
				self.password = result['password']
				self.updated_at = result['updated_at']
			else:
				result = db.queryOneRec(
						'''UPDATE users SET email=%s, name=%s, teachername=%s
							WHERE usersid=%s
							RETURNING updated_at''',
						(self.email, self.name, self.teachername, self.usersid)
					)
				self.updated_at = result['updated_at']
				
		else: 
			# It's a new users; insert it
			result = db.queryOneRec(
					'''INSERT INTO users (email,name,teachername,password) 
						VALUES (%s,%s,%s,MD5(%s))
						RETURNING usersid,created_at,updated_at,password''',
					(self.email,
					 self.name,
					 self.teachername,
					 self.password_plaintext + matconfig.password_salt)
				)
			self.created_at = result['created_at']
			self.password = result['password']
			self.updated_at = result['updated_at']
			self.usersid = result['usersid']

	# ===========================================================
	def setPassword(self,password_plaintext):
		''' Requires a "save()" after this is run to take effect '''
		self.password_plaintext = password_plaintext

	# ===========================================================
	def getCourses(self):
		ret = []
		query = '''SELECT c.*,cu.role AS role 
				FROM courses c 
				JOIN courses_users cu 
					ON c.coursesid = cu.coursesid 
				WHERE cu.usersid=%s AND cu.active AND c.active
				ORDER BY c.coursesid;'''
		courses = db.queryDictList(query,(self.usersid,))
		for c in courses:
			ret.append(course.Course(**c))
		return ret
