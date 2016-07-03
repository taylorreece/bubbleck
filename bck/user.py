#!/usr/bin/python3
import uuid
from bck import course, bckconfig
from bck.database import BckDB
from bck.bckobject import BckObject
db = BckDB()


# ===========================================================
def getUsers():
	''' Get all users '''
	return getUsersByID()

# ===========================================================
def getUsersByID(usersids=None):
	''' Get multiple user objects, return them in a list '''
	ret = []
	if usersids:
		query = 'SELECT * FROM users WHERE usersid IN %s AND active'
		result = db.query_dict_list(query, (usersids,))
	else: 
		query = 'SELECT * FROM users WHERE active'
		result = db.query_dict_list(query)
	for r in result:
		ret.append(User(**r))
	return ret

# ===========================================================
def getUserByID(usersid):
	return User.getUserByID(User(),usersid)

# ===========================================================
def getUserBySessionID(sessionid, ipaddress=None):
	# Update the user with their new IP.  updated_at will track last login time
	usersid = db.query_one_val('UPDATE sessions SET ipaddress=%s, updated_at=NOW() WHERE sessionid=%s RETURNING usersid',(ipaddress,sessionid))
	if usersid:
		return getUserByID(usersid)
	else:
		return None	

# ===========================================================
def getUserByEmailAndPassword(email,password):
	query = 'SELECT * FROM users WHERE email=%s AND password=MD5(%s) AND active'
	result = db.query_one_rec(query, (email, password+bckconfig.password_salt))
	if result:
		return User(**result)
	else:
		return User()

# ===========================================================
def getUserByResetKey(reset_key):
	query = 'SELECT * FROM users WHERE usersid=(SELECT usersid FROM password_reset WHERE key=%s)'
	result = db.query_one_rec(query, (reset_key,))
	if result:
		return User(**result)
	else:
		return None

# ===========================================================
def getUsersidByEmail(email):
	query = 'SELECT usersid FROM users WHERE email=%s AND active'
	return db.query_one_val(query, (email,))

# ===========================================================
class User(BckObject):
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
	logged_in = False

	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.set_attributes(kwargs)
		
	# ===========================================================
	def getUserByID(self,usersid):
		self.usersid = usersid
		result = db.query_one_rec('SELECT * FROM users WHERE usersid=%s AND active',(self.usersid,))
		if result:
			self.set_attributes(result)
			self._updateSessions()
			return self
		else:
			return None

	# ===========================================================
	def save(self):
		if self.usersid:
			# A user already exists; we're updating it.
			if self.password_plaintext:
				result = db.query_one_rec(
						'''UPDATE users SET email=%s, name=%s, teachername=%s, password=MD5(%s), active=%s, is_admin=%s
							WHERE usersid=%s
							RETURNING updated_at, password''',
						(self.email, 
						 self.name, 
						 self.teachername, 
						 self.password_plaintext + bckconfig.password_salt, 
						 self.active,
						 self.is_admin,
						 self.usersid)
					)
				self.set_attributes(result)
				self.updated_at = result['updated_at']
			else:
				result = db.query_one_rec(
						'''UPDATE users SET email=%s, name=%s, teachername=%s, active=%s, is_admin=%s
							WHERE usersid=%s
							RETURNING updated_at''',
						(self.email, self.name, self.teachername, self.active, self.is_admin, self.usersid)
					)
				self.set_attributes(result)
				
		else: 
			# It's a new users; insert it
			result = db.query_one_rec(
					'''INSERT INTO users (email,name,teachername,password,is_admin) 
						VALUES (%s,%s,%s,MD5(%s),%s)
						RETURNING usersid,created_at,updated_at,password,active''',
					(self.email,
					 self.name,
					 self.teachername,
					 self.password_plaintext + bckconfig.password_salt,
					 self.is_admin)
				)
			self.set_attributes(result)
		self._updateSessions()

	# ===========================================================
	def setPassword(self,password_plaintext):
		''' Requires a "save()" after this is run to take effect '''
		self.password_plaintext = password_plaintext

	# ===========================================================
	def checkPassword(self,password_plaintext):
		''' Check if the password supplied is the users current password '''
		return db.query_one_val("SELECT MD5(%s)=password FROM users WHERE usersid=%s", (password_plaintext + bckconfig.password_salt, self.usersid))
		
	# ===========================================================
	def getCourses(self):
		ret = []
		query = '''SELECT c.*,cu.role AS role 
				FROM courses c 
				JOIN courses_users cu 
					ON c.coursesid = cu.coursesid 
				WHERE cu.usersid=%s AND c.active
				ORDER BY c.coursesid;'''
		courses = db.query_dict_list(query,(self.usersid,))
		for c in courses:
			ret.append(course.Course(**c))
		return ret

	# ===========================================================
	def createSession(self, ipaddress):
		assert self.usersid
		sessionid = str(self.usersid) + str(uuid.uuid4())
		query = 'INSERT INTO sessions (usersid, sessionid, ipaddress) VALUES (%s,%s,%s)'
		db.query_no_results(query, (self.usersid, sessionid, ipaddress))
		self._updateSessions()
		return sessionid

	# ===========================================================
	def closeSession(self, sessionid):
		query = 'DELETE FROM sessions WHERE sessionid=%s AND usersid=%s RETURNING 1'
		return db.query_one_rec(query, (sessionid,self.usersid))

	# ===========================================================
	def getSubscriptionExpiration(self):
		query = 'SELECT NOW()>expiration AS expired, expiration FROM subscriptions WHERE usersid=%s AND active'
		return db.query_one_rec(query, (self.usersid,))
		
	# ===========================================================
	def deactivate(self):
		query = 'UPDATE users SET active=false WHERE usersid=%s'
		return db.query_no_results(query, (self.usersid,))

	# ===========================================================
	def generatePasswordResetKey(self):
		reset_key = str(self.usersid) + 'p' + str(uuid.uuid4())
		query = 'INSERT INTO password_reset (usersid, key) VALUES (%s,%s)'
		db.query_no_results(query, (self.usersid, reset_key))
		return reset_key

	# ===========================================================
	def _updateSessions(self):
		query = 'SELECT * FROM sessions WHERE usersid=%s ORDER BY updated_at DESC'
		self.sessions = db.query_dict_list(query, (self.usersid,))
		 
