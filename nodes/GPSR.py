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

state = 'waitForCommand'
object_list = {}
location_list = {}
current = [i for i in range(10)]

catagory_list = ['drink','food','cleaning stuff','snack','seating','utensil','table','shelf','appliance','bedroom','kitchen','hallway','living room']

def isCatagoryFound(data):
	for i in catagory_list:
		if(i in data):
			return i
	return None

def isObjectFound(data):
	for i in object_list.keys():
		if(i in data):
			return i
	return None

def isLocationFound(data):
	for i in location_list.keys():
		if(i in data):
			return i
	return None

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
	global state,current
	if(delay.isWait()): return None
	rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'waitForCommand'):
		publish.pan_tilt_command(getQuaternion(0,0,0))
		if(device == 'voice'):
			#current[2] = isLocationFound(data)
			#current[3] = isObjectFound(data)
			if('go' in data and isCatagoryFound(data) != None):
				current[0] = 'go'
				current[1] = isCatagoryFound(data)
			        call(['espeak','you say go to ' + isCatagoryFound(data) + ' yes or no' ,'-ven+f4','-s 120'])
				state = 'confirm'
			elif('move' in data and isCatagoryFound(data) != None):
				current[0] = 'go'
				current[1] = isCatagoryFound(data)
			        call(['espeak','you say move to ' + isCatagoryFound(data) + ' yes or no','-ven+f4','-s 120'])
				state = 'confirm'
			elif('head' in data and isCatagoryFound(data) != None):
				current[0] = 'go'
				current[1] = isCatagoryFound(data)
			        call(['espeak','you say head to ' + isCatagoryFound(data) + ' yes or no','-ven+f4','-s 120'])
				state = 'confirm'
			elif('bring' in data and isCatagoryFound(data) != None):
				current[0] = 'bring'
				current[1] = isCatagoryFound(data)
			        call(['espeak','you say bring you ' + isCatagoryFound(data) + ' yes or no','-ven+f4','-s 120'])
				state = 'confirm'
			elif('take' in data and isCatagoryFound(data) != None):
				current[0] = 'bring'
				current[1] = isCatagoryFound(data)
			        call(['espeak','you say take ' + isCatagoryFound(data) + ' to you yes or no','-ven+f4','-s 120'])
				state = 'confirm'
	elif(state == 'confirm'):
		if(device == 'voice'):
			if('robot yes' in data):
				if(current[0] == 'go'):
					call(['espeak','please tell me what ' + current[1] + ' to go','-ven+f4','-s 120'])
				elif(current[0] == 'bring'):
					call(['espeak','please tell me what ' + current[1] + ' to bring','-ven+f4','-s 120'])
				state = 'inspection'
			elif('robot no' in data):
				call(['espeak','please say again ','-ven+f4','-s 120'])
				state = 'waitForCommand'
	elif(state == 'inspection'):
		if(device == 'voice'):
			if(current[0] == 'go' and isLocationFound(data) != None):
				current[2] = isLocationFound(data)
				call(['espeak','you want me to go ' + current[2] + ' yes or no','-ven+f4','-s 120'])
				state = 'confirmInspection'
			elif(current[0] == 'bring' and isObjectFound(data) != None):
				current[2] = isObjectFound(data)
				call(['espeak','you want me to bring ' + current[2] + ' yes or no','-ven+f4','-s 120'])
				state = 'confirmInspection'
	elif(state == 'confirmInspection'):
		if(device == 'voice'):
			if('robot yes' in data):
				call(['espeak','i will do it ','-ven+f4','-s 120'])
				delay.delay(5)
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(1)
				if(current[0] == 'go'):
					current[3] = current[2]
					publish.base.publish(location_list[current[2]])
				elif(current[0] == 'bring'):
					current[3] = object_list[current[2]].place
					publish.base.publish(location_list[object_list[current[2]].place])
				delay.delay(2)
				state = 'gotoPoint'
			elif('robot no' in data):
				if(current[0] == 'go'):
					call(['espeak','please tell me what ' + current[1] + ' to go','-ven+f4','-s 120'])
				elif(current[0] == 'bring'):
					call(['espeak','please tell me what ' + current[1] + ' to bring','-ven+f4','-s 120'])
				state = 'inspection'
	elif(state == 'gotoPoint'):
		if(device == 'base' and data == 'SUCCEEDED'):
			call(['espeak','i am at ' + current[3] + ' i found nothing i go back','-ven+f4','-s 120'])
			publish.base.publish(location_list['start_pos'])
			delay.delay(2)
			state = 'gotoStart'
		if(device == 'base' and data == 'ABORTED'):
			call(['espeak','i am at ' + current[3] + ' i found nothing i go back','-ven+f4','-s 120'])
			publish.base.publish(location_list['start_pos'])
			delay.delay(2)
			state = 'gotoStart'
	elif(state == 'gotoStart'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 'waitForCommand'
				

		
			

def main():

    rospy.loginfo('Start State')
    rospy.init_node('main_state')

    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.Subscriber("/object/output", String, cb_object)

    publish.manipulator_action.publish(String('walking'))
    rospy.spin()

if __name__ == '__main__':
    try:
	delay = Delay()
	publish = Publish()
        readObject(object_list)
	readLocation(location_list)
        main()
    except rospy.ROSInterruptException:
        pass
