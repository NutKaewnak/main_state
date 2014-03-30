#!/usr/bin/env python
import rospy
import roslib
import time
from subprocess import call
roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.base_state import *
from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Quaternion, Pose2D
from math import pi

location_list = {}

class RIPS(BaseState):
	def __init__(self):
		BaseState.__init__(self)

		Publish.set_height(1.27)
		rospy.loginfo('Start RIPS State')
		rospy.spin()

	def main(self, device, data):
		rospy.loginfo("state:"+self.state+" from:"+device+" data:"+str(data))
		if(self.state == 'init'):
			if(device == 'door' and data == 'open'):
				# move pass door
				Publish.move_relative(1.5,0)
				self.state = 'passDoor'
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			publish.manipulator_action.publish(String('walking'))
		elif(state == 'passDoor'):
			if(device == 'base' and data == 'SUCCEEDED'):
				state = 'gotoTable'
				# send to base
				publish.base.publish(location_list['register_pos'])
		elif(state == 'gotoTable'):
			if(device == 'base' and data == 'SUCCEEDED'):
				state = 'moveArm'
				# send to arm
				publish.manipulator_action.publish(String('rips_out'))
				publish.pan_tilt_command(getQuaternion(0,0,0))
				call(["espeak","-ven+f4","Hello Sir,My name is lumyai,i came from kasetsart university thailand.i am a robot from planet earth came here to service you please accept this registration","-s 120"])
		elif(state == 'moveArm'):
			if(device == 'manipulator' and data == 'finish'):
				state = 'waitForCommand'
				
		elif(state == 'waitForCommand'):
			if(device == 'voice'):
				if(data == 'get out'):
					state = 'arm out'
					# send to arm
					publish.manipulator_action.publish(String('walking'))
		elif(state == 'arm out'):
			if(device == 'manipulator' and data == 'finish'):
				# send to pan_tilt
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(2)
				# send to base
				publish.base.publish(location_list['outside_pos'])
				state = 'get out'

		elif(state == 'set neck'):
			if(device == 'servo' and data == 'finish'):
				# send to base
				publish.base.publish(location_list['outside_pos'])
				state = 'get out'
		elif(state == 'get out'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			publish.manipulator_action.publish(String('walking'))
			if(device == 'base' and data == 'SUCCEEDED'):
				state = 'finish'

if __name__ == '__main__':
    try:
    	rospy.init_node('main_state')
	RIPS()
    except Exception, error:
        print str(error)
