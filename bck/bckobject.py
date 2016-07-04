class BckObject(object):
	''' Generic BubbleCK object to be used by exam, course, etc '''
	def set_attributes(self, mydict):
		'''Accepts a dictionary of attributes; sets them on the object'''
		for key,value in mydict.items():
			setattr(self,key,value)
