#!usr/bin/env python
import rospy
import roslib
roslib.load_manifest('main_state')

from std_msgs.msg import String
from delay import *

class Devices:
	door='door'
	base='base'
	manipulator='manipulator'
	voice='voice'

class BaseState:
	def __init__(self):
		rospy.Subscriber('/door/is_open', String, self.CallbackDoor)
		rospy.Subscriber('/base/is_fin', String, self.CallbackBase)
		rospy.Subscriber('/manipulator/is_fin', String, self.CallbackManipulator)
		rospy.Subscriber('/voice/output', String, self.CallbackVoice)

		self.delay = Delay()
		self.state = 'init'

	def CallbackDoor(self,data):
		self.main(Devices.door,data.data)

	def CallbackBase(self,data):
		self.main(Devices.base,data.data)
		
	def CallbackManipulator(self,data):
		self.main(Devices.manipulator,data.data)
		
	def CallbackVoice(self,data):
		self.main(Devices.voice,data.data)

	def main(self,device,data):
		pass
		

if __name__ == '__main__':
	try:
		BaseState()
	except Exception, error:
		print str(error)
	
