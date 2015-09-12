import psycopg2
import psycopg2.extras
from settings import dbname, dbuser

class mat_db:
	_db_conn = None
	_db_cur = None

	def __init__(self):
		pass

	def _connect(self):
		self._db_conn = psycopg2.connect(database=dbname,user=dbuser)
		self._db_cur = self._db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	def _disconnect(self):
		self._db_conn.commit()
		self._db_cur.close()
		self._db_conn.close()

	def query(self,query,args,one_record=False):
		self._connect()
		result = self._db_cur.execute(query,args)
		if one_record:
			ret = self._db_cur.fetchone()
		else:
			ret = self._db_cur.fetchall()
		self._disconnect()
		return ret
	
	def queryOneVal(self,query,args=None):
		ret = self.query(query,args,one_record=True)
		try:
			return ret[0]
		except:
			return None

	def queryOneRec(self,query,args=None):
		return self.query(query,args,one_record=True)
	
	def queryDictList(self,query,args):
		return self.query(query,args)
