import os 
  
# Normal file system 
paths = os.listdir(os.path.dirname(__file__)) 
__all__ = [f[:-3] for f in paths if os.path.isfile(f) and f.endswith('.py')] 
__all__.extend([f for f in paths if os.path.isdir(f)])
