import os 
  
if '__loader__' in locals(): 
	# Loading from a zip file 
	zipfiles = __loader__._files 
	__all__ = [zipfiles[file][0] for file in zipfiles.keys() if file.endswith('.pyc')] 
	__all__ = [name.split('\\')[-1] for name in __all__] # get filename 
	__all__ = map(lambda __all__: __all__[:-4], __all__) # chop off '.pyc' 
else: 
	# Normal file system 
	paths = os.listdir(os.path.dirname(__file__)) 
	__all__ = [f[:-3] for f in paths if os.path.isfile(f) and f.endswith('.py')] 
	__all__.extend([f for f in paths if os.path.isdir(f)])
