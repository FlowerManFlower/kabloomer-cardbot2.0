import time
import math

class Countdown:
	def __init__(self):
		self.start_time = None
		self.limit = 0
		self.started = False

	def start(self, time_limit):
		if(self.started):
			return
		self.start_time = time.time()
		self.limit = time_limit
		self.started = True

	def hasStarted(self):
		return(self.started)

	def timePassed(self):
		if(self.start_time is None):
			return(None)
		return(math.floor(time.time() - self.start_time))

	def timeRemaining(self):
		if(self.start_time is None):
			return(None)
		return(math.floor(self.limit - self.timePassed()))

	def isFinished(self):
		if(not self.hasStarted()):
			return(True)
		if(self.timePassed() > self.limit):
			self.started = False
			return(True)
		return(False)
