#!/usr/bin/env python
import rospy
import roslib
import time
from subprocess import call
roslib.load_manifest('main_state')

from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D,Vector3

state = 'init'
#state = 'getCommand'
pub = {}
living_room = NavGoalMsg('clear','absolute',Pose2D(1.682,3.214,0.647))
bar_pos = NavGoalMsg('clear','absolute',Pose2D(-4.805,10.542,2.490))
startTime = 0
current_pos = 0
peopleobjectCount = 0
objectName = []
peopleName = []
peoplePos = []
people_name = ['michael' ,'christopher' ,'matthew' ,'joshua' ,'david' ,'james' ,'daniel' ,'robert' ,'john' ,'joseph' ,'jessica' ,'jennifer' ,'amanda' ,'ashley' ,'sarah' ,'stephanie' ,'melissa' ,'nicole' ,'elizabeth' ,'heather']
object_name = ['green tea' ,'energy drink' ,'banana juice' ,'sprite' ,'coffee' ,'cappuccino' ,'max coffee']
temp = []

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

def main_state(device,data):
	global state,pub,startTime,current_pos,objectName,peopleName,peoplePos,peopleobjectCount,temp
	rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'init'):
		if(device == 'door' and data == 'open'):
			state = 'gotoLivingRoom'
			# send to base
			pub["base"].publish(living_room)			
	elif(state == 'gotoLivingRoom'):
		if(device == 'base' and data == 'SUCCEEDED'):
			#################################################IK : Need to fix the gesture delay
			state = 'searchGesture'
			startTime = time.localtime()
	elif(state == 'searchGesture'):
		if(device == 'gesture'):
			# x,y = from gesture
                        x,y,z = data.split(',')
			pub["base"].publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),0.3)))
			peoplePos.append(data)	
			state = 'getCommand'
		#################################################IK : Need to fix the gesture delay
		stopTime = time.localtime()
		if(time.mktime(stopTime)-time.mktime(startTime) >= 10.0):
			pub["base"].publish(NavGoalMsg('clear','relative',Pose2D(0.0,0.0,0.3)))			
	elif(state == 'getCommand'):
		if(device == 'base' and data == 'SUCCEEDED'):
			peopleName.append('')
			objectName.append('')
			call(['espeak','Hello,What is your name','-ven+f4','-s 150'])
			state = 'waitForName'
	elif(state == 'waitForName'):
		if(device == 'voice'):
			for i in people_name:
				if(i in data):
					call(['espeak','Are you ' + i,'-ven+f4','-s 150'])
					temp = i
					state = 'ConfirmName'
				# send to base
                        	#pub['base'].publish(object_pos[current_pos])
	elif(state == 'ConfirmName'):
		if(device == 'voice' and 'yes' in data):
			peopleName[peopleobjectCount] = temp
			call(['espeak','Hello '+temp +' what do you want to drink','-ven+f4','-s 150'])
			state = 'waitForObject'
		elif(device == 'voice' and 'no' in data):
			call(['espeak','Hello,What is your name','-ven+f4','-s 150'])
			state = 'waitForName'
	elif(state == 'waitForObject'):
		if(device == 'voice'):
			for i in object_name:
				if(i in data):
					call(['espeak','you want ' + i +' yes or no ','-ven+f4','-s 150'])
					temp = i
					state = 'ConfirmObject'
	elif(state == 'ConfirmObject'):
		if(device == 'voice' and 'yes' in data):
			objectName[peopleobjectCount] = temp
			call(['espeak','i will bring you ' + temp,'-ven+f4','-s 150'])
			peopleobjectCount+=1
			if(peopleobjectCount==3):	
				pub["base"].publish(bar_pos)	
				state = 'gotoBar'
			else:
				state = 'searchGesture'
				#################################################IK : Need to fix the gesture delay
				startTime = time.localtime()
		elif(device == 'voice' and 'no' in data):
			call(['espeak','Hello '+ peopleName[peopleobjectCount] +' what do you want to drink','-ven+f4','-s 150'])
			state = 'waitForObject'
	elif(state == 'gotoBar'):	
		if(device == 'base' and data == 'SUCCEEDED'):
			# searching
			publish.object_search.publish(objectName[0])
			state = 'waitForSearch'
	elif(state == 'waitForSearch'):
		if(device == 'object'):
			if(data == 'no'):
				call(['espeak','I cannot find '+ objectName[0] +'.please help me','-ven+f4','-s 150'])
				publish.manipulator_action.publish(String('grip_open'))
				delay.delay(5)
				publish.manipulator_action.publish(String('grip_close'))
				state = 'getObject'
			else:
				objectName,x,y,z = data.split(',')
			        call(['espeak','i found' + objectName[0],'-ven+f4'])
                        	publish.manipulator_point.publish(Vector3(float(x),float(y),float(z)))
				state = 'getObject'
	elif(state == 'getObject'):
		if(device == 'manipulator' and data == 'finish'):
			publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
			delay.delay(2)
			x,y,z = data.split(',')
			pub["base"].publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),0.3)))
			state = 'gotoPlace'
	elif(state == 'gotoPlace'):
		if(device == 'base' and data == 'SUCCEEDED'):
			checkpeople()
			state = 'detectpeople'

	elif(state == 'detectpeople'):
		#########detectpeople
		if(device == 'x' and data == 'SUCCEEDED'):
			state = 'left'
			# send to arm
			call(['espeak','This is '+objectName[0]+' you ordered. '+peopleName[0] +' please recieve','-ven+f4','-s 150'])
			publish.manipulator_action.publish(String('drop'))
		else:
			call(['espeak','I cannot find '+peopleName[0] +'.please wave your hand','-ven+f4','-s 150'])
			#################################################IK : Need to fix the gesture delay
			state = 'searchGestureDrop'
			startTime = time.localtime()
	elif(state == 'searchGestureDrop'):
		if(device == 'gesture'):
			# x,y = from gesture
                        x,y,z = data.split(',')
			pub["base"].publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),0.3)))
			state = 'gotoPlace'
		#################################################IK : Need to fix the gesture delay
		stopTime = time.localtime()
		if(time.mktime(stopTime)-time.mktime(startTime) >= 10.0):
			pub["base"].publish(NavGoalMsg('clear','relative',Pose2D(0.0,0.0,0.3)))	
	elif(state == 'left'):
		if(device == 'manipulator' and data == 'finish'):
			objectName.remove(0)
			peopleName.remove(0)
			peoplePos.remove(0)
			peopleobjectCount -= 1
			if(peopleobjectCount == 0):
				# send to base
				publish.pan_tilt_command(getQuaternion(0,50*pi/180,0))
				delay.delay(2)
                        	publish.base.publish(location_list['outside_pos'])
				state = 'get out'
			else:
				pub["base"].publish(bar_pos)	
				state = 'gotoBar'
	elif(state == 'get out'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 'finish'

def main():
    pub['base'] = rospy.Publisher('/base/set_pos', NavGoalMsg)
    pub['object_point'] = rospy.Publisher('/object_point', Vector3)
    pub['manipulator'] = rospy.Publisher('/manipulator/action', String)
    pub['start_search'] = rospy.Publisher('/object/start_search', String)
    rospy.init_node('main_state')
    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/gesture/point", String, cb_gesture)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
