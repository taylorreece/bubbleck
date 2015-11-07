#!/usr/bin/python3
import random
from bck import studentexam
from bck.database import BckDB
from bck.bckobject import BckObject
db = BckDB()

def getExamByID(examsid):
	return Exam.getExamByID(Exam(),examsid)

class Exam(BckObject):
	active = None
	answers = None
	coursesid = None
	created_at = None
	examsid = None
	layout = None
	name = None
	show_coursename = True
	show_directions = True
	show_points = True
	show_teachername = True
	updated_at = None

	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.setAttributes(kwargs)

	# ===========================================================
	def getExamByID(self,examsid):
		self.examsid = examsid
		result = db.queryOneRec('SELECT * FROM exams WHERE examsid=%s',(self.examsid,))
		if result:
			self.setAttributes(result)
			return self
		else:
			return None

	# ===========================================================
	def save(self):
		if self.examsid:
			# It already has an ID; update it
			query = ''' UPDATE exams SET name=%s,
						     coursesid=%s,
						     answers=%s,
						     layout=%s,
						     show_coursename=%s,
						     show_directions=%s,
						     show_points=%s,
						     show_teachername=%s,
						     active=%s
					WHERE examsid=%s 
					RETURNING updated_at'''
			result = db.queryOneRec(query, (self.name, 
							self.coursesid,
							self.answers, 
							self.layout, 
							self.show_coursename, 
							self.show_directions, 
							self.show_points,
							self.show_teachername,
							self.active,
							self.examsid)
			)
			self.setAttributes(result)
		else:
			query = ''' INSERT INTO exams 
					(name,coursesid,answers,layout,show_coursename,show_directions,show_points,show_teachername)
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
					RETURNING created_at, updated_at, examsid, active'''
			result = db.queryOneRec(query, (self.name,
							self.coursesid,
							self.answers,
							self.layout, 
							self.show_coursename, 
							self.show_directions, 
							self.show_points,
							self.show_teachername)
			)
			self.setAttributes(result)

	# ===========================================================
	def getShareKeys(self):
		query = 'SELECT key FROM examshares WHERE examsid=%s AND active'
		return db.queryOneValList(query,(self.examsid,))

	# ===========================================================
	def getDeactivatedKeys(self):
		query = 'SELECT key FROM examshares WHERE examsid=%s AND NOT active'
		return db.queryOneValList(query,(self.examsid,))
	
	# ===========================================================
	def addShareKey(self):
		ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		# a key is comprised of the examsid, with leading zeros to make it 10 digits
		# plus a jumble of 16 random figures.  In theory, there'll never be collision.
		# Is this right way to do it?  Hell no.  Is it the fast way?  Yeah....
		sharekey = '%010d' % self.examsid + ''.join(random.choice(ALPHABET) for i in range(16))
		query = 'INSERT INTO examshares (examsid, key) VALUES (%s,%s)'
		db.queryNoResults(query,(self.examsid,sharekey))
		return sharekey

	# ===========================================================
	def deactivateShareKey(self,key):
		query = 'UPDATE examshares SET active=False WHERE key=%s AND examsid=%s'
		db.queryNoResults(query,(key, self.examsid))

	# ===========================================================
	def activateShareKey(self,key):
		query = 'UPDATE examshares SET active=True WHERE key=%s AND examsid=%s'
		db.queryNoResults(query,(key, self.examsid))

	# ===========================================================
	def getStudentExams(self):
		ret = []
		query = 'SELECT * FROM studentexams WHERE examsid=%s AND active'
		studentexams = db.queryDictList(query,(self.examsid,))
		for s in studentexams:
			ret.append(studentexam.StudentExam(**s))
		return ret
