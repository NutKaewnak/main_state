#!/usr/bin/env python
import rospy
import roslib
import time
roslib.load_manifest('main_state')

from std_msgs.msg import String, Float64, Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Quaternion, Pose2D, Vector3

class Publish(object):

    	base = rospy.Publisher('/base/set_pos', NavGoalMsg)
    	manipulator_point = rospy.Publisher('/manipulator/object_point_split', Vector3)
	manipulator_action = rospy.Publisher('/manipulator/action', String)
	object_search = rospy.Publisher('/object/search', String)
	pan_tilt_cmd = rospy.Publisher('/pan_tilt_cmd', Quaternion)
	follow_init = rospy.Publisher('/follow/init', Bool)
	height_cmd = rospy.Publisher('/height_cmd', Float64)
	
	def __init__(self):
		pass
	
	def pan_tilt_command(self,data):
		self.pan_tilt_cmd.publish(data)
    
	def height_command(self,data):
		self.height_cmd.publish(Float64(data))
	
	def robot_stop(self):
		self.base.publish(NavGoalMsg('stop','absolute',Pose2D(0.0,0.0,0.0)))
		
