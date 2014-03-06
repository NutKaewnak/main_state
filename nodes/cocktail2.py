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
from geometry_msgs.msg import Pose2D,Vector3,PointStamped
from math import pi
from math import sin,cos

state = 'init'
#state = 'searchGesture'
location_list = {} 
object_list = ['pringles','lay','water','orange juice','green tea','milk','s','fanta','corn flakes','corn']
#currentObject = 0
objectName = ''
peopleName = ''
people_name = ['richard','rishard','richart','philip' ,'emma' ,'danial' ,'tina','steve' ,'henry' ,'peter','peeter' ,'robert' ,'sarah' ,'brian' ,'thomas','britney' ,'justin','tony' ,'kevin' ,'joseph','michael' ,'michelle' ,'donna']
temp = []
currentAngle = -90*pi/180
taskList = []


currentNum = 0
currentObjectNumber = 0
object_mapping = {}
desiredObject = 0
currentObject = []
movingTime = 2
currentTime = 0
#objectName = None
objectPoint = Vector3()
locationName = ''
isInit = False


def manipulateInitialize():
	heightCmdPublisher.publish(Float64(1.31))
	tiltKinectCmdPublisher.publish(Float64(-0.40))
	delay.delay(3)

def normalInitialize():
	heightCmdPublisher.publish(Float64(1.21))
	tiltKinectCmdPublisher.publish(Float64(-0.40))
	delay.delay(3)
	

def cb_objectDepthPoint(data):
	print "get objectPoint at (" + str(data.x) + "," + str(data.y) + "," + str(data.z) + ")"
	global objectPoint
	objectPoint.x = data.x
	objectPoint.y = data.y
	objectPoint.z = data.z-0.15
	#execute_state(objectPoint)
	#call(["espeak","-ven+f4","get depth point","-s 150"])

def cb_numberObject(data):
	global currentObjectNumber
	print "object_number : " + data.data
	currentObjectNumber = int(data.data)

def cb_objectPoint(data):
#	tmp = data.split(' ')
#	x = data.x
#	y = data.y
#	z = data.z
#	rospy.loginfo('(' + str(x) + ',' + str(y) + ',' + str(z) + ')')
#	execute_state("finding object's point succeeded")

	#print "in cb_objectPoint at state = " + state + " with data : " + data.data 

	#if state == 'GET_OBJECT':
	#	execute_state('recognition',data.data)
	execute_state('recognition',data.data)


def cb_door(data):
    main_state('door',data.data)

def cb_voice(data):
    main_state('voice',data.data)

def cb_manipulator(data):
    main_state('manipulator',data.data)

def cb_gesture(data):
    main_state('gesture',"%f,%f,%f" % (data.point.x,data.point.y,data.point.z))

def cb_base(data):
    main_state('base',data.data)

def cb_object(data):
    main_state('object',data.data)

def main_state(device,data):

	global currentNum, currentObjectNumber, currentObject,currentTime, desiredObject, movingTime
	global state,currentAngle,temp,peopleName,objectName,taskList
	if(delay.isWait()): return None
	rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'init'):
		if(device == 'door' and data == 'open'):
			# move pass door
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(1.5,0,0)))
			delay.delay(1)
			state = 'passDoor'
		if(!isInit):
			normalInitialize()
			publish.manipulator_action.publish(String('walking'))
			isInit = True

	elif(state == 'passDoor'):
		if(device == 'base' and data == 'SUCCEEDED'):
			# send to base
			publish.base.publish(location_list['kitchen_room'])
			delay.delay(3)
			state = 'gotoKitchenRoom'

	elif(state == 'gotoKitchenRoom'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
			call(['espeak','Please wave your hand.','-ven+f4','-s 150'])
			delay.waiting(3)
			#delay.delay(3)
			state = 'searchGesture'

	elif(state == 'searchGesture'):
		if(device == 'gesture'):
			# x,y = from gesture
			x,y,z = data.split(',')
			#print 'Kinect angle : ' + str(currentAngle)
			x = float(z) * cos(currentAngle)
			y = float(z) * sin(currentAngle)
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),currentAngle)))
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(1)
			state = 'getCommand'
		if(delay.isWaitFinish()):
			currentAngle += 0.3
			publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
			delay.waiting(3)
			if(currentAngle >= 90*pi/180):
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(1)
				call(['espeak','I did not found anyone.','-ven+f4','-s 150'])
				#publish.base.publish(location_list['bar'])			
				state = 'error'
	elif(state == 'getCommand'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			delay.delay(1)
			call(['espeak','Hello, What is your name.','-ven+f4','-s 150'])
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
			call(['espeak','Hello '+temp +' what do you want','-ven+f4','-s 150'])
			state = 'waitForObject'
		elif(device == 'voice' and 'no' in data):
			call(['espeak','Hello,What is your name','-ven+f4','-s 150'])
			state = 'waitForName'

	elif(state == 'waitForObject'):
		if(device == 'voice'):
			for i in object_list:
				if(i in data):
					call(['espeak','you want ' + i +' yes or no ','-ven+f4','-s 150'])
					temp = i
					state = 'ConfirmObject'
					break
	elif(state == 'ConfirmObject'):
		if(device == 'voice' and 'yes' in data):
			#desiredObject = object_mapping[objectName]
			objectName = temp
			call(['espeak','where is ' + objectName,'-ven+f4','-s 150'])
			objectName = temp
			#call(['espeak','i will bring you ' + temp,'-ven+f4','-s 150'])
			#taskList.append([peopleName,objectName])
			#publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			#delay.delay(1)

			manipulateInitialize()
			# go to move base
			#publish.base.publish(location_list['bar_table_pos_'+str(currentTime)])

			state  = "waitForLocation"
		elif(device == 'voice' and 'no' in data):
			call(['espeak','Hello '+peopleName +' what do you want','-ven+f4','-s 150'])
			state = 'waitForObject'
#			if(len(taskList) == 3):
#				publish.base.publish(location_list['bar'])			
#				state = 'getDrink_moving'
#			else:
#				# send to base
#				publish.base.publish(location_list['living_room'])
#				delay.delay(1)				
#				state = 'gotoLivingRoom'
				
	elif(state == 'waitForLocation'):
		if(device == 'voice'):
			for i in location_list:
				if(i in data):
					call(['espeak','is '+objectName+' is on the ' + i +'. yes or no.','-ven+f4','-s 150'])
					#call(['espeak','where is ' + objectName,'-ven+f4','-s 150'])
					temp = i
					state = 'ConfirmLocation'
					break
	elif(state == 'ConfirmLocation'):
		if(device == 'voice' and 'yes' in data):
			#desiredObject = object_mapping[objectName]
			#objectName = temp
			call(['espeak','i will go to ' + temp,'-ven+f4','-s 150'])
			#taskList.append([peopleName,objectName])
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(1)

			heightCmdPublisher.publish(Float64(1.21))
			tiltKinectCmdPublisher.publish(Float64(-0.40))
			delay.delay(1)
# go to move base
			publish.base.publish(location_list[temp])

			state  = "MOVE_BASE"

#			if(len(taskList) == 3):
#				publish.base.publish(location_list['bar'])			
#				state = 'getDrink_moving'
#			else:
#				# send to base
#				publish.base.publish(location_list['living_room'])
#				delay.delay(1)				
#				state = 'gotoLivingRoom'
		elif(device == 'voice' and 'no' in data):
			call(['espeak','where is ' + objectName,'-ven+f4','-s 150'])
			state = 'waitForLocation'

	elif(state == 'MOVE_BASE'):	
		if(device == 'base' and data == 'SUCCEEDED'):
			call(['espeak','I reach the destination.','-ven+f4','-s 150'])
			currentObjectNumber  = 0
			state = "GET_OBJECT"
			delay.delay(2)
			findObjectPointPublisher.publish(String("start"));

	elif state == 'GET_OBJECT':
		if(device == 'recognition'):

			currentNum+=1
			print "currentNum : " + str(currentNum) + " currentObjectNumber : " + str(currentObjectNumber)
			print "currentObject.append(" + str(data) + ")"

			#call(["espeak","-ven+f4","ting","-s 250"])
			call(["aplay","/home/skuba/skuba_athome/main_state/sound/accept.wav"])
			currentObject.append(data)
			if (currentNum == currentObjectNumber):
				currentNum = 0
				for tmp in currentObject:
					print tmp
				for tmp in currentObject:
					elements = tmp.split(' ')
					if desiredObject == int(elements[0]):
						vec = Vector3()
						vec.x = float(elements[1])
						vec.y = float(elements[2])
						state = 'FINISH'
						print "ITEM FOUND at pixel ("+ str(vec.x) + "," + str(vec.y)+")"
						call(["espeak","-ven+f4",objectName + " found. I will get it.","-s 150"])
						toClickObjectPublisher.publish(vec)

						manipulateInitialize()
						#heightCmdPublisher.publish(Float64(1.3))
						#heightCmdPublisher.publish(Float64(1.41))
						#delay.waiting(2)
						#print "before delay count"
						#delay.delay(2)
						#print "after delay count"

						pickObjectPublisher.publish(objectPoint)
						state = "PICK_OBJECT"
						call(["aplay","/home/skuba/skuba_athome/main_state/sound/nomessage.wav"])
						return 0

				if( currentTime < movingTime):
					call(["espeak","-ven+f4",objectName + "go to next position","-s 150"])
					rospy.loginfo("go to next position")
					#state = 'ERROR'
					#publish.base.publish(NavGoalMsg('clear','relative',Pose2D(0,0.2,0)))
					publish.base.publish(location_list['bar_table_pos_'+str(currentTime)])
					currentTime += 1
					state = 'MOVE_BASE'
				else:
					state = 'ERROR'

	elif state == "PICK_OBJECT":
		if(device == 'manipulator' and data == 'finish'):
			call(["espeak","-ven+f4","I got it","-s 150"])
			#heightCmdPublisher.publish(Float64(1.1))
			normalInitialize()
			#heightCmdPublisher.publish(Float64(1.21))
			#tiltKinectCmdPublisher.publish(Float64(-0.40))
			state = 'GO_TO_LIVING_ROOM_WITH_OBJECT'
			publish.base.publish(location_list['living_room'])

	elif state == "GO_TO_LIVING_ROOM_WITH_OBJECT":
		if(device == 'base' and data == 'SUCCEEDED'):
			call(["espeak","-ven+f4",peopleName + ". please wave your hand.","-s 150"])
			publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
			delay.waiting(3)
			state = 'SEARCH_GESTURE_WITH_OBJECT'

	elif state == 'SEARCH_GESTURE_WITH_OBJECT':
		if(device == 'gesture'):
			# x,y = from gesture
                        x,y,z = data.split(',')
			x = float(z) * cos(currentAngle)
			y = float(z) * sin(currentAngle)
			publish.base.publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),currentAngle)))
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(1)
			state = 'SERVER_ORDER'
		if(delay.isWaitFinish()):
			currentAngle += 0.3
			publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
			delay.waiting(7)
			if(currentAngle >= 90*pi/180):
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(1)
				call(["espeak","-ven+f4","lost master","-s 150"])
				#publish.base.publish(location_list['bar'])			
				#state = 'getDrink_moving'
	elif(state == 'SERVER_ORDER'):
		if(device == 'base' and data == 'SUCCEEDED'):
			publish.pan_tilt_command(getQuaternion(0,0,0))
			delay.delay(1)
			call(['espeak','This is your order. please take it.','-ven+f4','-s 150'])
			delay.delay(5)
			publish.manipulator_action.publish(String('walking'))
			delay.delay(3)
			publish.base.publish(location_list['out_side'])			
			state = 'get out'

	elif(state == 'get out'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 'finish'

def main():

    object_mapping['green tea'] = 1
    object_mapping['water'] = 2
    object_mapping['est'] = 3
    object_mapping['fanta'] = 4
    object_mapping['corn flakes'] = 5
    object_mapping['lay'] = 6
    object_mapping['pringles'] = 7
    object_mapping['milk'] = 8
    object_mapping['orange juice'] = 9
    object_mapping['milo'] = 10


    rospy.loginfo('Start Main_state')
    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/gesture/point", PointStamped, cb_gesture)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.Subscriber("/object/output", String, cb_object)


    rospy.Subscriber("/verified_result", String, cb_objectPoint)
    #rospy.Subscriber("/voice/output", String, cb_voice)
    #rospy.Subscriber("/base/is_fin", String, cb_base)
    #rospy.Subscriber("/findCenter", Vector3, cb_findCenter)
    #rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator_response)
    #rospy.Subscriber("/manipulator/is_fin", String, cb_manipulate)
    rospy.Subscriber("object_number", String, cb_numberObject)
    rospy.Subscriber("/object_depth_point", Vector3, cb_objectDepthPoint)


    rospy.spin()

if __name__ == '__main__':
    try:
    	rospy.init_node('main_state')
	delay = Delay()
	publish = Publish()
	findObjectPointPublisher = rospy.Publisher('/localization', String)
	toClickObjectPublisher = rospy.Publisher('/click_depth_point', Vector3)
	pickObjectPublisher = rospy.Publisher('/object_point', Vector3)
	heightCmdPublisher = rospy.Publisher('/height_cmd', Float64)
	tiltKinectCmdPublisher = rospy.Publisher('/tilt_kinect/command', Float64)
	#readObject(object_list)
	readLocation(location_list)
        main()
    except rospy.ROSInterruptException:
        pass
