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
#state = 'gotoObject'
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
			return None
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
			state = 'gotoCommand'
			# send to base
			publish.base.publish(location_list['command_pos'])
	elif(state == 'gotoCommand'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			state = 'waitForCommand'
	elif(state == 'waitForCommand'):
		if(device == 'voice'):
			if('living room' in data):
				# send to base
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				publish.height_command(location_height_list[current.pos()])
				delay.delay(2)
                        	publish.base.publish(location_list[current.current_location])
				delay.delay(1)
				state = 'gotoObject'
	elif(state == 'gotoObject'):
		if(device == 'base' and data == 'SUCCEEDED'):
			reconfig.changeDepthResolution(2)
			delay.delay(1)
			# searching
			publish.object_search.publish(current.object_name())
			state = 'waitForSearch'
	elif(state == 'waitForSearch'):
		if(device == 'object'):
			if(data == 'no'):
				temp = current.object_name()
				if(temp == None):
					reconfig.changeDepthResolution(8)
					temp = current.pos()
					if(temp == None):
						# send to base
                        			publish.base.publish(location_list['outside_pos'])
						delay.delay(1)
						state = 'get out'
					else:
						publish.height_command(location_height_list[current.current_location])
						# send to base
                        			publish.base.publish(location_list[current.current_location])
						delay.delay(1)
						state = 'gotoObject'
				else:
					publish.object_search.publish(temp)
			else:
				state = 'getObject'
				objectName,x,y,z = data.split(',')
			        call(['espeak','i found' + current.current_object,'-ven+f4','-s 120'])
                        	publish.manipulator_point.publish(Vector3(float(x),float(y),float(z)))
				delay.delay(3)
	elif(state == 'getObject'):
		if(device == 'manipulator' and data == 'finish'):
			reconfig.changeDepthResolution(8)
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			publish.height_command(location_height_list[object_list[current.current_object].place])
			delay.delay(1)
                        publish.base.publish(location_list[object_list[current.current_object].place])
			delay.delay(1)
			state = 'gotoPlace'
		if(device == 'manipulator' and data == 'error'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			publish.height_command(location_height_list[current.pos()])
			delay.delay(2)
                        publish.base.publish(location_list[current.current_location])
			delay.delay(1)
			state = 'gotoObject'
	elif(state == 'gotoPlace'):
		if(device == 'base' and data == 'SUCCEEDED'):
			# send to arm
			if(object_list[current.current_object].catagory == 'cleaning stuff'):
				publish.manipulator_action.publish(String('drophallwaytable'))
				delay.delay(1)
			# send to arm
			elif(object_list[current.current_object].catagory == 'drink'):
				publish.manipulator_action.publish(String('dropbar'))
				delay.delay(1)
			elif(object_list[current.current_object].catagory == 'food'):
				publish.manipulator_action.publish(String('dropstove'))
				delay.delay(1)
			elif(object_list[current.current_object].catagory == 'snacks'):
				publish.manipulator_action.publish(String('dropsidetable'))
				delay.delay(1)
			else:
				publish.manipulator_action.publish(String('dropbar'))
				delay.delay(1)
			
			state = 'left'
	elif(state == 'left'):
		if(device == 'manipulator' and data == 'finish'):
			current._object = 0
			temp = current.pos()
			if(temp == None):
				# send to base
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(1)
                        	publish.base.publish(location_list['outside_pos'])
				delay.delay(1)
				state = 'get out'
			else:
				# send to base
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				publish.height_command(location_height_list[current.current_location])
				delay.delay(1)
                        	publish.base.publish(location_list[current.current_location])
				delay.delay(1)
				state = 'gotoObject'
	elif(state == 'get out'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 'finish'

		

def main():
    global current
    current = Current(search_sequence,object_list.keys())

    rospy.loginfo('Start State')

    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.Subscriber("/object/output", String, cb_object)

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
	readLocationHeight(location_height_list)
	readLocationSequence(search_sequence)
        main()
    except rospy.ROSInterruptException:
        pass
