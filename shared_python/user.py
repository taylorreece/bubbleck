#!/usr/bin/python
from mat import course, matconfig
from mat.database import MatDB
from mat.matobject import MatObject
db = MatDB()


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

def getUserBySessionID(sessionid):
	usersid = db.queryOneVal('SELECT usersid FROM sessions WHERE sessionid=%s',(sessionid,))
	if usersid:
		return getUserByID(usersid)
	else:
		return None	

class User(MatObject):
	active = True
	created_at = None
	email = None
	is_admin = False
	name = None
	password = None
	password_plaintext = None
	teachername = None
	updated_at = None
	usersid = None
	sessions = []

	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.setAttributes(kwargs)
		
	# ===========================================================
	def getUserByID(self,usersid):
		self.usersid = usersid
		result = db.queryOneRec('SELECT * FROM users WHERE usersid=%s',(self.usersid,))
		if result:
			self.setAttributes(result)
			self._updateSessions()
			return self
		else:
			return None

	# ===========================================================
	def save(self):
		if self.usersid:
			# A user already exists; we're updating it.
			if self.password_plaintext:
				result = db.queryOneRec(
						'''UPDATE users SET email=%s, name=%s, teachername=%s, password=MD5(%s), active=%s, is_admin=%s
							WHERE usersid=%s
							RETURNING updated_at, password''',
						(self.email, 
						 self.name, 
						 self.teachername, 
						 self.password_plaintext + matconfig.password_salt, 
						 self.active,
						 self.is_admin,
						 self.usersid)
					)
				self.setAttributes(result)
				self.updated_at = result['updated_at']
			else:
				result = db.queryOneRec(
						'''UPDATE users SET email=%s, name=%s, teachername=%s, active=%s, is_admin=%s
							WHERE usersid=%s
							RETURNING updated_at''',
						(self.email, self.name, self.teachername, self.active, self.is_admin, self.usersid)
					)
				self.setAttributes(result)
				
		else: 
			# It's a new users; insert it
			result = db.queryOneRec(
					'''INSERT INTO users (email,name,teachername,password,is_admin) 
						VALUES (%s,%s,%s,MD5(%s),%s)
						RETURNING usersid,created_at,updated_at,password,active''',
					(self.email,
					 self.name,
					 self.teachername,
					 self.password_plaintext + matconfig.password_salt,
					 self.is_admin)
				)
			self.setAttributes(result)
		self._updateSessions()

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
				WHERE cu.usersid=%s AND c.active
				ORDER BY c.coursesid;'''
		courses = db.queryDictList(query,(self.usersid,))
		for c in courses:
			ret.append(course.Course(**c))
		return ret

	# ===========================================================
	def createSession(self):
		assert self.usersid
		sessionid = self.usersid + uuid.uuid4()
		query = 'INSERT INTO sessions (usersid, sessionid) VALUES (%s,%s)'
		db.queryNoResults(query, (self.usersid, sessionid))
		self._updateSessions()
		return sessionid

	# ===========================================================
	def deleteSession(self, sessionid):
		query = 'DELETE FROM sessions WHERE sessionsid=%s'
		db.queryNoResults(query, (sessionid))

	# ===========================================================
	def _updateSessions(self):
		query = 'SELECT sessionid FROM sessions WHERE usersid=%s'
		self.sessions = db.queryOneValList(query, (self.usersid,))
		 

