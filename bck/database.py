import psycopg2
import psycopg2.extras
from bck.bckconfig import dbname, dbuser, dbhost, dbpass

class BckDB(object):
	''' Database object used by the other classes to interface with the database '''
	_db_conn = None
	_db_cur = None

	# ===========================================================
	def __init__(self):
		pass

	# ===========================================================
	def _connect(self):
		self._db_conn = psycopg2.connect(database=dbname,user=dbuser,host=dbhost,password=dbpass)
		self._db_cur = self._db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# ===========================================================
	def _disconnect(self):
		self._db_conn.commit()
		self._db_cur.close()
		self._db_conn.close()

	# ===========================================================
	def get_schema_version(self):
		query = "SELECT value FROM settings WHERE category='schema' AND name='version'"
		return self.query_one_val(query)

	# ===========================================================
	def run_file(self,f):
		self.query(query = f.read(), args=None, return_results=False)

	# ===========================================================
	def query(self,query,args,one_record=False,return_results=True):
		''' Basic function that taps in to postgres to run a query with some set of args '''
		self._connect()
		result = self._db_cur.execute(query,args)
		if return_results:
			if one_record:
				ret = self._db_cur.fetchone()
			else:
				ret = self._db_cur.fetchall()
		self._disconnect()
		if return_results:
			return ret
		return

	# ===========================================================
	def query_no_results(self,query,args=None):
		'''
		For UPDATEs, DELETEs, etc that dont need results returned
		'''
		self.query(query,args,return_results=False)

	# ===========================================================
	def query_one_val(self,query,args=None):
		'''
		For snagging a single value from the database
		For example, SELECT value FROM settings WHERE name=blah
		'''
		ret = self.query(query,args,one_record=True)
		try:
			return ret[0]
		except:
			return None

	# ===========================================================
	def query_one_rec(self,query,args=None):
		'''
		Grabs a single record.  e.g. SELECT * FROM users WHERE usersid=1
		'''
		return self.query(query,args,one_record=True)

	# ===========================================================
	def query_dict_list(self,query,args=None):
		'''
		Grabs multiple records; returns list of dictionaries.
		e.g. SELECT * FROM users
		'''
		return self.query(query,args)

	# ===========================================================
	def query_one_val_list(self,query,args=None):
		'''
		For snagging a list of values from the database.  Returns a list instead of a dict.
		Fore example, SELECT coursesid FROM courses WHERE usersid=1
		'''
		ret = self.query(query,args)
		try:
			return [x[0] for x in ret]
		except:
			return None
