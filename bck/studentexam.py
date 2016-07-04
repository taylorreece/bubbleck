#!/usr/bin/python3
from bck.database import BckDB
from bck.bckobject import BckObject
db = BckDB()

class StudentExam(BckObject):
	''' An object representation of a scanned in student exam '''
	active = None
	answers = None
	created_at = None
	examsid = None
	sectionsid = None
	studentexamsid = None
	updated_at = None
	
	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.set_attributes(kwargs)

	# ===========================================================
	def save(self):
		if self.studentexamsid:
			# It already has an ID; update it
			query = ''' UPDATE studentexams SET answers=%s,
						     examsid=%s,
						     sectionsid=%s,
						     active=%s
					WHERE studentexamsid=%s 
					RETURNING updated_at'''
			result = db.query_one_rec(query, (self.answers, 
							self.examsid,
							self.sectionsid,
							self.active,
							self.studentexamsid)
			)
			self.set_attributes(result)
		else:
			query = ''' INSERT INTO studentexams 
					(answers,examsid,sectionsid)
					VALUES (%s,%s,%s)
					RETURNING created_at, updated_at, studentexamsid, active'''
			result = db.query_one_rec(query, (self.answers,
							self.examsid,
							self.sectionsid)
			)
			self.set_attributes(result)
