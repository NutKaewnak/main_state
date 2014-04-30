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
from geometry_msgs.msg import Pose2D,Vector3
from diagnostic_msgs.msg import DiagnosticArray
from math import pi

state = 'init'
object_list = {}
location_list = {}
location_height_list = {}
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
		self.current_location = self.search_sequence[self._pos]
		self.current_object = self.object_list[self._object]

	def pos(self):
		if(self._pos >= len(search_sequence)):
			self._pos = 0
		self.current_location = self.search_sequence[self._pos]
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

def cb_people(data):
    main_state('people',data.data)

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
	elif(state == 'passDoor'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 'gotoCommand'
			# send to base
			publish.base.publish(location_list['kitchen_emer'])
	elif(state == 'gotoCommand'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.waiting(70)
			state = 'waitForCommand'
	elif(state == 'waitForCommand'):
		if(delay.isWaitFinish()):
			# send to base
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
			state = 'gotoObject'
	elif(state == 'gotoObject'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			delay.waiting(10)
			state = 'waitForSearch'
		elif(device == 'base' and data == 'ABORTED'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
	elif(state == 'waitForSearch'):
		if(device == 'people'):
			x,y,z = data.split(',')
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),atan(float(y)/float(x)))))
			state = 'checkPeople'
		if(delay.isWaitFinish()):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
			state = 'gotoObject'
	elif(state == 'checkPeople'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			call(['espeak','are you alright','-ven+f4','-s 120'])
			delay.waiting(10)
			state = 'confirmAnswer'
		elif(device == 'base' and data == 'ABORTED'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
			state = 'gotoObject'
	elif(state == 'confirmAnswer'):
		if(device == 'voice' and data == 'yes'):
			call(['espeak','please follow me to the exit','-ven+f4','-s 120'])
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list['exit'])
			delay.delay(1)
			state = 'gotoExit'
		elif(device == 'voice' and data == 'no'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
			state = 'gotoObject'
		if(delay.isWaitFinish()):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
			state = 'gotoObject'
	elif(state == 'gotoExit'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
                        publish.base.publish(location_list[current.pos()])
			delay.delay(1)
			state = 'gotoObject'

def main():
    global current
    current = Current(search_sequence,object_list.keys())

    rospy.loginfo('Start State')

    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.Subscriber("/object/output", String, cb_object)
    rospy.Subscriber("/people/point", String, cb_people)

    publish.height_command(1.27)
    publish.manipulator_action.publish(String('walking'))
    rospy.spin()

if __name__ == '__main__':
    try:
    	rospy.init_node('main_state')
	delay = Delay()
	publish = Publish()
	reconfig = Reconfig()

	readObject(object_list)	
	readLocation(location_list)
	readLocationSequenceEmer(search_sequence)
        main()
    except rospy.ROSInterruptException:
        pass
