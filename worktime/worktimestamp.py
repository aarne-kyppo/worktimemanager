from datetime import *
from datetime import time
class WorkTimeStamp():
	def __init__(self,isEnd, year, month, day, hour, minute):
		self.isEnd = isEnd
		self.datetimeobject = datetime(int(year),int(month),int(day),int(hour),int(minute))
