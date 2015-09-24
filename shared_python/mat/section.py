#!/usr/bin/python
from mat.database import MatDB
from mat.matobject import MatObject
db = MatDB()

class Section(MatObject):
	active = None
	created_at = None
	coursesid = None
	name = None
	sectionsid = None
	updated_at = None

	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.setAttributes(kwargs)

	# ===========================================================
	def save(self):
		if self.sectionsid:
			# It already has an ID; update it
			query = ''' UPDATE sections SET name=%s,
						     coursesid=%s,
						     active=%s
					WHERE sectionsid=%s 
					RETURNING updated_at'''
			result = db.queryOneRec(query, (self.name, 
							self.coursesid,
							self.active,
							self.sectionsid)
			)
			self.setAttributes(result)
		else:
			query = ''' INSERT INTO sections 
					(name,coursesid)
					VALUES (%s,%s)
					RETURNING created_at, updated_at, sectionsid, active'''
			result = db.queryOneRec(query, (self.name,
							self.coursesid)
			)
			self.setAttributes(result)
