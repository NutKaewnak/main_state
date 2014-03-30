#!/usr/bin/env python
import time

class Delay:
	def __init__(self):
		self.start_time = time.localtime()
		self.period = 0
		self.wait_period = 0

	# in second
	def delay(self,period):
		self.start_time = time.localtime()
		self.period = period
		time.sleep(period)
        
        def waiting(self,period):
		self.wait_period = period
		self.start_time = time.localtime()
		time.sleep(1)

	def isWaitFinish(self):
		current_time = time.localtime()
		if(time.mktime(current_time)-time.mktime(self.start_time) >= self.wait_period):
			return True
		return False
	
	def isWait(self):
		current_time = time.localtime()
		if(time.mktime(current_time)-time.mktime(self.start_time) >= self.period):
			return False
		return True

if __name__ == "__main__":
	object_list = {}
	readObject(object_list)
	print object_list
	location_list = {}
	readLocation(location_list)
	print location_list
	
