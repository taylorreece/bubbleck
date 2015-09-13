#!/usr/bin/python
from mat.database import MatDB
from mat.matobject import MatObject
db = MatDB()

def getExamByID(examsid):
	return Exam.getExamByID(Exam(),examsid)

class Exam(MatObject):
	active = None
	answers = None
	coursesid = None
	created_at = None
	examsid = None
	layout = None
	name = None
	show_coursename = None
	show_directions = None
	show_teachername = None
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
		else:
			return None

		
