#!/usr/bin/python
from database import mat_db

db = mat_db()

class User(object):
	usersid = None
	email = None
	password = None
	name = None
	teachername = None
	created_at = None
	updated_at = None
	def __init__(self, *args, **kwargs):
		# Multiple ways to initialize this object
		if kwargs.get('usersid'):
			self.usersid = kwargs.get('usersid')
			result = db.queryOneRec('SELECT * FROM users WHERE usersid=%s',(self.usersid,))
			if result:
				self.email = result['email']
				self.password = result['password']
				self.name = result['name']
				self.teachername = result['teachername']
				self.created_at = result['created_at']
				self.updated_at = result['updated_at']
			else:
				return None
		else:
			self.email = kwargs.get('email')
			self.name = kwargs.get('name')
			self.teachername = kwargs.get('teachername')
			self.password = kwargs.get('password')
	def save(self):
		result = db.queryOneRec(
				'''INSERT INTO users (email,name,teachername,password) 
					VALUES (%s,%s,%s,MD5(%s))
					RETURNING usersid,created_at,updated_at,password''',
				(self.email,self.name,self.teachername,self.password)
			)
		self.usersid = result['usersid']
		self.password = result['password']
		self.created_at = result['created_at']
		self.updated_at = result['updated_at']
