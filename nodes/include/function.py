#!/usr/bin/env python
import rospy
import roslib
import time
roslib.load_manifest('main_state')

import tf
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Quaternion,Pose2D

class Delay:
	def __init__(self):
		self.start_time = time.localtime()
		self.period = 0
		self.wait_period = 0

	# in second
	def delay(self,period):
		self.start_time = time.localtime()
		self.period = period
		time.sleep(period)
        
        def waiting(self,period):
		self.wait_period = period
		self.start_time = time.localtime()
		time.sleep(1)

	def isWaitFinish(self):
		current_time = time.localtime()
		if(time.mktime(current_time)-time.mktime(self.start_time) >= self.wait_period):
			return True
		return False
	
	def isWait(self):
		current_time = time.localtime()
		if(time.mktime(current_time)-time.mktime(self.start_time) >= self.period):
			return False
		return True

class a_object:
	def __init__(self,name,catagory,place):
		self.name = name
		self.catagory = catagory
		self.place = place
      
	def __repr__(self):
		return 'name: ' + self.name + "\ncatagory: " + self.catagory + "\nplace: " + self.place

	def __str__(self):
		return 'name: ' + self.name + "\ncatagory: " + self.catagory + "\nplace: " + self.place

def getQuaternion(roll,pitch,yaw):
    temp = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    return Quaternion(temp[0],temp[1],temp[2],temp[3])

def readObject(object_list):
	rospy.loginfo('Main : Read Object')
	temp = open(roslib.packages.get_pkg_dir('main_state')+'/config/object_catagory.txt')
	catagory,place = '',''
	for line in temp:
		line = line.strip().split('-')
		if(len(line) == 1):
			line = line[0].split(',')
			catagory,place = line[0],line[1]
		else:
			object_list[line[1]] = a_object(line[1],catagory,place)

def readLocation(location_list):
	rospy.loginfo('Main : Read Location')
	temp = open(roslib.packages.get_pkg_dir('main_state')+'/config/location.txt')
	for line in temp:
		if(line.strip() == ''): continue
		line = line.strip().split(',')
		location_list[line[0]] = NavGoalMsg('clear','absolute',Pose2D(float(line[1]),float(line[2]),float(line[3])))

def readLocation(location_list,filename):
	rospy.loginfo('Main : Read Location')
	temp = open(roslib.packages.get_pkg_dir('main_state')+filename)
	for line in temp:
		if(line.strip() == ''): continue
		line = line.strip().split(',')
		location_list[line[0]] = NavGoalMsg('clear','absolute',Pose2D(float(line[1]),float(line[2]),float(line[3])))


def readLocationHeight(location_height_list):
	rospy.loginfo('Main : Read Location Height')
	temp = open(roslib.packages.get_pkg_dir('main_state')+'/config/location.txt')
	for line in temp:
		if(line.strip() == ''): continue
		line = line.strip().split(',')
		location_height_list[line[0]] = float(line[4])

def readLocationSequenceEmer(location_list):
	rospy.loginfo('Main : Read Location Sequence')
	temp = open(roslib.packages.get_pkg_dir('main_state')+'/config/search_sequence_emer.txt')
	for line in temp:
		if(line.strip() == ''): continue
		location_list.append(line.strip())



def readLocationSequence(location_list):
	rospy.loginfo('Main : Read Location Sequence')
	temp = open(roslib.packages.get_pkg_dir('main_state')+'/config/search_sequence.txt')
	for line in temp:
		if(line.strip() == ''): continue
		location_list.append(line.strip())

if __name__ == "__main__":
	object_list = {}
	readObject(object_list)
	print object_list
	location_list = {}
	readLocation(location_list)
	print location_list
	
