#!/usr/bin/env python
# TODO generate voice , Manipulate , color Tracking
import rospy
import roslib
import time
import math
from subprocess import call
roslib.load_manifest('main_state')
roslib.load_manifest('manipulator')
from include.function import *
#from include.publish import *
from std_msgs.msg import String,Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Vector3
state = 'init'
#state = 'searching'
startTime = 0
count = 0
points = []
value = ''
def cb_voice(data):
	main_state('voice',data.data)

def cb_color_track(data):
	main_state('color_track',data)

def cb_mani(data):
	main_state('manipulate',data.data)

def cb_object_point(data):
	main_state('object',data.data)

def main_state(device,data):
	global state,startTime,count,points,value
	rospy.loginfo("state:"+state+" from:"+device+" "+str(data))
	if(state == 'init'):
		if(device == 'voice' and ('bring' in data)):
			call(["espeak","-ven+f4","i will make you a breakfast","-s 150"])
			findObjectPointPublisher.publish('start')#start searching object
			state = 'searching'
	elif(state =='searching'):
		if(device == 'object'):
			call(["espeak","-ven+f4","Searching ingredients","-s 150"])
			vector_split = data.split(',')
			print vector_split
			for tmp in vector_split[:-1]:
				points.append(map(float,tmp.split(' ')))
			print 'points : ' + str(points)

			min_value = 999
			value = None
			for tmp in points:
				if min_value > tmp[1]:
					min_value = tmp[1]
					value = tmp

			value = "%f %f %f" % (value[0],value[1],value[2]) 
			state = 'grasp'
			point_pub_vec_split.publish(value) # send vector3 point to grasp object
	elif(state == 'grasp'):
		#point_pub_vec_split.publish(value) # send vector3 point to grasp object
		if(device == 'manipulate' and data == 'finish'):
			state = 'track'

	elif(state == 'track'):
		call(["espeak","-ven+f4","searching a bowl","-s 150"])
		if(device == 'color_track'):
			send_object_point.publish(data)#send point above a bowl to pour
			call(["espeak","-ven+f4","pouring","-s 150"])
			state = 'serve'

	elif(state == 'serve'):
		if(device == 'manipulate' and data == 'finish'):
			call(["espeak","-ven+f4","breakfast is served","-s 150"])
			act.publish('walking_for_drop')
			state = 'drop'

	elif(state == 'drop'):
		#send normal action and release grasping
		if(device == 'manipulate' and data == 'finish'):
			state = 'finish'

	elif(state == 'finish'):
		pass
		
def main():
	global findObjectPointPublisher,send_object_point,point_pub_vec,point_pub_vec_split,act
	rospy.init_node('thailand_openchallange2014')
	rospy.Subscriber("/Tracking", Vector3 , cb_color_track) #Tracking (point x,y,z)
	rospy.Subscriber("/manipulator/is_fin", String, cb_mani)#manipulate (string 'isfin' ?)
	rospy.Subscriber("/voice/output", String, cb_voice)#voice
	rospy.Subscriber("/center_pcl_object", String, cb_object_point)#Recieve object point (String x,y,z,x,y,z)

	act = rospy.Publisher('/manipulator/action',String)
	send_object_point = rospy.Publisher('/manipulator/object_point',Vector3)#transform
	findObjectPointPublisher = rospy.Publisher('/localization', String)#trigger to start track object
	point_pub_vec = rospy.Publisher('/manipulator/object_point', Vector3)
	point_pub_vec_split = rospy.Publisher('/manipulator/object_point_split', String)

	rospy.spin()

if __name__ == '__main__':
    try:
		delay = Delay()
		#publish = Publish()
		main()
    except rospy.ROSInterruptException:
		pass
