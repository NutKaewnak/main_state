#!/usr/bin/env python
import rospy
import roslib
import time
from subprocess import call
roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.reconfig_kinect import *
from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Quaternion, Pose2D
from math import pi

state = 'init'
location_list = {}

def cb_door(data):
    main_state('door',data.data)

def cb_voice(data):
    main_state('voice',data.data)

def cb_manipulator(data):
    main_state('manipulator',data.data)

def cb_base(data):
    main_state('base',data.data)

def main_state(device,data):
	global state
	if(delay.isWait()): return None
	rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'init'):
		if(device == 'door' and data == 'open'):
			# move pass door
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(1.5,0,0)))
			state = 'passDoor'
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

		

def main():
    rospy.loginfo('Start Main_state')
    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/voice/output", String, cb_voice)
    #rospy.Subscriber("/diagnostics", DiagnosticArray, cb_servo)
    publish.height_command(1.27)
    rospy.spin()

if __name__ == '__main__':
    try:
    	rospy.init_node('main_state')
	delay = Delay()
	publish = Publish()
	reconfig = Reconfig()
	readLocation(location_list)
        main()
    except rospy.ROSInterruptException:
        pass
