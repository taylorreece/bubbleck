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

