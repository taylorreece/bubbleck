#!/usr/bin/python3
from bck.database import BckDB
from bck.bckobject import BckObject
db = BckDB()

class StudentExam(BckObject):
	active = None
	answers = None
	created_at = None
	examsid = None
	sectionsid = None
	studentexamsid = None
	updated_at = None
	
	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.setAttributes(kwargs)

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
			result = db.queryOneRec(query, (self.answers, 
							self.examsid,
							self.sectionsid,
							self.active,
							self.studentexamsid)
			)
			self.setAttributes(result)
		else:
			query = ''' INSERT INTO studentexams 
					(answers,examsid,sectionsid)
					VALUES (%s,%s,%s)
					RETURNING created_at, updated_at, studentexamsid, active'''
			result = db.queryOneRec(query, (self.answers,
							self.examsid,
							self.sectionsid)
			)
			self.setAttributes(result)
