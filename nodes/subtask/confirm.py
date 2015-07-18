__author__ = 'jamjann'
import rospy
import roslib
from include.base_state import *

class Confirm:
	def __init__(self):
    	BaseState.__init__(self)
    	rospy.loginfo('Confirm State')
    	self.conversation = None
    	rospy.spin()

    def toConfirm(conversation):
    	self.conversation = conversation
    	self.state = STATE.INIT

	def main(self, device, data):
		if self.conversation is None:
			return

		rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
		if self.state is STATE.INIT:
			if device is Devices.voice:
				if data is 'robot yes':
					self.state = STATE.SUBMIT
				elif data is 'robot no':
					self.state = STATE.CANCEL
				else:
					self.speak("I do not understand  , please tell me again")
		else:
			self.conversation = None


if __name__ is '__main__':
    Confirm()