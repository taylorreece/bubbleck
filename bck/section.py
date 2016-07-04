#!/usr/bin/python3
from bck.database import BckDB
from bck.bckobject import BckObject
db = BckDB()

def getSectionByID(sectionsid):
	return Section.getSectionByID(Section(),sectionsid)

class Section(BckObject):
	''' An object representation of a section instance '''
	active = None
	created_at = None
	coursesid = None
	name = None
	sectionsid = None
	updated_at = None

	# ===========================================================
	def __init__(self, *args, **kwargs):
		self.set_attributes(kwargs)

	# ===========================================================
	def save(self):
		if self.sectionsid:
			# It already has an ID; update it
			query = ''' UPDATE sections SET name=%s,
						     coursesid=%s,
						     active=%s
					WHERE sectionsid=%s 
					RETURNING updated_at'''
			result = db.query_one_rec(query, (self.name, 
							self.coursesid,
							self.active,
							self.sectionsid)
			)
			self.set_attributes(result)
		else:
			query = ''' INSERT INTO sections 
					(name,coursesid)
					VALUES (%s,%s)
					RETURNING created_at, updated_at, sectionsid, active'''
			result = db.query_one_rec(query, (self.name,
							self.coursesid)
			)
			self.set_attributes(result)

	# ===========================================================
	def getSectionByID(self,sectionsid):
		self.sectionsid = sectionsid
		result = db.query_one_rec('SELECT * FROM sections WHERE sectionsid=%s',(self.sectionsid,))
		if result:
			self.set_attributes(result)
			return self
		else:
			return None 
	
	# ===========================================================
	def deactivate(self):
		query = 'UPDATE sections SET active=false WHERE sectionsid=%s'
		return db.query_no_results(query, (self.sectionsid,))

