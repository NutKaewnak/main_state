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
from math import pi

state = 'init'
#state = 'searchGesture'
location_list = {} 
object_list = {}
currentObject = 0
objectName = ''
peopleName = ''
people_name = ['michael' ,'christopher' ,'matthew' ,'joshua' ,'daniel','david' ,'andrew' ,'james' ,'justin' ,'joseph' ,'jessica' ,'ashley','brittany' ,'amanda','samantha' ,'sarah' ,'stephanie','jennifer' ,'elizabeth' ,'lauren']
temp = []
currentAngle = -90*pi/180
taskList = []

def cb_door(data):
    main_state('door',data.data)

def cb_voice(data):
    main_state('voice',data.data)

def cb_manipulator(data):
    main_state('manipulator',data.data)

def cb_gesture(data):
    main_state('gesture',data.data)

def cb_base(data):
    main_state('base',data.data)

def cb_object(data):
    main_state('object',data.data)

def main_state(device,data):
	global state,currentAngle,temp,peopleName,objectName,taskList,currentObject
	if(delay.isWait()): return None
	rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'init'):
		if(device == 'door' and data == 'open'):
			# move pass door
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(1.5,0,0)))
			delay.delay(1)
			state = 'passDoor'
		publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
                publish.manipulator_action.publish(String('walking'))
	elif(state == 'passDoor'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 'gotoLivingRoom'
			# send to base
			publish.base.publish(location_list['living_room'])
	elif(state == 'gotoLivingRoom'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
			delay.waiting(7)
			state = 'searchGesture'
	elif(state == 'searchGesture'):
		if(device == 'gesture'):
			# x,y = from gesture
                        x,y,z = data.split(',')
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),currentAngle)))
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(1)
			state = 'getCommand'
		if(delay.isWaitFinish()):
			currentAngle += 0.3
			publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
			delay.waiting(7)
			if(currentAngle >= 90*pi/180):
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(1)
				publish.base.publish(location_list['bar'])			
				state = 'getDrink_moving'
	elif(state == 'getCommand'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			delay.delay(1)
			call(['espeak','Hello What is your name','-ven+f4','-s 150'])
			state = 'waitForName'
	elif(state == 'waitForName'):
		if(device == 'voice'):
			for i in people_name:
				if(i in data):
					call(['espeak','Are you ' + i,'-ven+f4','-s 150'])
					temp = i
					state = 'ConfirmName'
					break
	elif(state == 'ConfirmName'):
		if(device == 'voice' and 'yes' in data):
			peopleName = temp
			call(['espeak','Hello '+temp +' what do you want to drink','-ven+f4','-s 150'])
			state = 'waitForObject'
		elif(device == 'voice' and 'no' in data):
			call(['espeak','Hello,What is your name','-ven+f4','-s 150'])
			state = 'waitForName'
	elif(state == 'waitForObject'):
		if(device == 'voice'):
			for i in object_list.keys():
				if(i in data):
					call(['espeak','you want ' + i +' yes or no ','-ven+f4','-s 150'])
					temp = i
					state = 'ConfirmObject'
					break
	elif(state == 'ConfirmObject'):
		if(device == 'voice' and 'yes' in data):
			objectName = temp
			call(['espeak','i will bring you ' + temp,'-ven+f4','-s 150'])
			taskList.append([peopleName,objectName])
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(1)
			if(len(taskList) == 3):
				publish.base.publish(location_list['bar'])			
				state = 'getDrink_moving'
			else:
				# send to base
				publish.base.publish(location_list['living_room'])
				delay.delay(1)				
				state = 'gotoLivingRoom'
				
				
		elif(device == 'voice' and 'no' in data):
			call(['espeak','Hello '+ peopleName +' what do you want to drink','-ven+f4','-s 150'])
			state = 'waitForObject'
	elif(state == 'getDrink_moving'):	
		if(device == 'base' and data == 'SUCCEEDED'):
			if(currentObject >= len(taskList)):
				publish.base.publish(location_list['outside_pos'])
				state = 'get out'
			else:
				#search
				publish.object_search.publish(taskList[currentObject][1])
				state = 'getDrink_searching'
	elif(state == 'getDrink_searching'):
		if(device == 'object'):
			if(data == 'no'):
				currentObject += 1
				state = 'getDrink_moving'
			else:
				objectName,x,y,z = data.split(',')
                        	publish.manipulator_point.publish(Vector3(float(x),float(y),float(z)))
				state = 'getDrink' 
	elif(state == 'getDrink'):
		if(device == 'manipulator' and data == 'finish'):
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
    rospy.Subscriber("/gesture/point", String, cb_gesture)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.Subscriber("/object/output", String, cb_object)
    rospy.spin()

if __name__ == '__main__':
    try:
    	rospy.init_node('main_state')
	delay = Delay()
	publish = Publish()
        readObject(object_list)
	readLocation(location_list)
        main()
    except rospy.ROSInterruptException:
        pass
