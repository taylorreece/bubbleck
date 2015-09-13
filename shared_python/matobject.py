class MatObject(object):
	def setAttributes(self, mydict):
		'''Accepts a dictionary of attributes; sets them on the object'''
		for key,value in mydict.iteritems():
			setattr(self,key,value)
