#!/usr/bin/env python
import rospy
import roslib
import time
from subprocess import call
roslib.load_manifest('main_state')

from include.function import *
from include.publish import *

from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D,Vector3
from diagnostic_msgs.msg import DiagnosticArray
from math import pi

state = 'init'
object_list = {}
location_list = {}
search_sequence = []
current = []

class Current(object):
	object_list = []
	search_sequence = []
	
	def __init__(self,search_sequence,object_list):
		self._pos = 0
		self._object = 0
		self.object_list = object_list
		self.search_sequence = search_sequence

	def pos(self):
		if(self._pos >= len(search_sequence)):
			return None
		self._pos += 1
		return self.search_sequence[self._pos-1]
	
	def object_name(self):
		if(self._object >= len(object_list)):
			return None
		self.current_object = self.object_list[self._object]
		self._object += 1
		return self.object_list[self._object-1]

def cb_door(data):
    main_state('door',data.data)

def cb_voice(data):
    main_state('voice',data.data)

def cb_manipulator(data):
    main_state('manipulator',data.data)

def cb_base(data):
    main_state('base',data.data)

def cb_object(data):
    main_state('object',data.data)

def main_state(device,data):
	global state
	if(delay.isWait()): return None
	rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'init'):
		if(device == 'door' and data == 'open'):
			# move pass door
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(1.5,0,0)))
			delay.delay(1)
			state = 'passDoor'
		publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
		publish.manipulator_action.publish(String('opencwalking'))
	elif(state == 'passDoor'):
		if(device == 'base' and data == 'SUCCEEDED'):
			# send to base
			publish.base.publish(location_list['oc_pos'])
			delay.delay(1)
			state = 'gotoCommand'
	elif(state == 'gotoCommand'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			state = 'waitForCommand'
	elif(state == 'waitForCommand'):
		if(device == 'voice'):
			if('kitchen' in data):
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(1)
				# send to base
                        	publish.base.publish(location_list['kitchen'])
				delay.delay(1)
				state = 'gotoKitchen'
	elif(state == 'gotoKitchen'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.manipulator_action.publish(String('opencliftup'))
			state = 'waitForGoback'
	elif(state == 'waitForGoback'):
		if(device == 'voice'):
			if('living room' in data):
				publish.manipulator_action.publish(String('opencwalking'))
				state = 'waitPullBack'
	elif(state == 'waitPullBack'):
		if(device == 'manipulator' and data == 'finish'):
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			        publish.base.publish(location_list['oc_pos'])
				state = 'finish'

		

def main():
    global current
    current = Current(search_sequence,object_list.keys())

    rospy.loginfo('Start State')
    rospy.init_node('main_state')

    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.Subscriber("/object/output", String, cb_object)

    publish.manipulator_action.publish(String('normal'))
    rospy.spin()

if __name__ == '__main__':
    try:
	delay = Delay()
	publish = Publish()
        readObject(object_list)
	readLocation(location_list)
	readLocationSequence(search_sequence)
        main()
    except rospy.ROSInterruptException:
        pass
