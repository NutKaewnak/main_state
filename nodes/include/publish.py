#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import *
from lumyai_navigation_msgs.msg import *
from geometry_msgs.msg import *
from function import *
from subprocess import call

roslib.load_manifest('main_state')

class Publish:
    base = rospy.Publisher('/base/set_pos', NavGoalMsg)
    manipulator_point = rospy.Publisher('/manipulator/object_point_split', Vector3)
    manipulator_action = rospy.Publisher('/manipulator/action', String)
    object_search = rospy.Publisher('/object/search', String)
    pan_tilt_cmd = rospy.Publisher('/pan_tilt_cmd', Quaternion)
    follow_init = rospy.Publisher('/follow/init', Bool)
    height_cmd = rospy.Publisher('/height_cmd', Float64)

    def __init__(self):
        pass

    @staticmethod
    def set_height(data):
        Publish.height_cmd.publish(Float64(data))

    @staticmethod
    def move_relative(x, y):
        Publish.base.publish(NavGoalMsg('clear', 'relative', Pose2D(float(x), float(y), 0.0)))

    @staticmethod
    def set_neck(roll, pitch, yaw):
        Publish.pan_tilt_cmd.publish(getQuaternion(float(roll), float(pitch), float(yaw)))

    @staticmethod
    def set_manipulator_action(action):
        Publish.manipulator_action(String(str(action)))

    @staticmethod
    def move_absolute(pose):
        Publish.base.publish(NavGoalMsg('clear', 'absolute', pose))

    @staticmethod
    def speak(message):
        call(["espeak", "-ven+f4", message, "-s 120"])

    def robot_stop(self):
        self.base.publish(NavGoalMsg('stop', 'absolute', Pose2D(0.0, 0.0, 0.0)))