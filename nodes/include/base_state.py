#!usr/bin/env python
import rospy
import roslib
from location import *
from delay import *
from publish import *
from reconfig_kinect import *
from subprocess import Popen

roslib.load_manifest('main_state')

from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D

class Devices:
    door = 'door'
    base = 'base'
    manipulator = 'manipulator'
    voice = 'voice'
    follow = 'follow'

class BaseState:
    def __init__(self):
        rospy.Subscriber('/door/is_open', String, self.callback_door)
        rospy.Subscriber('/base/is_fin', String, self.callback_base)
        rospy.Subscriber('/manipulator/is_fin', String, self.callback_manipulator)
        rospy.Subscriber('/voice/output', String, self.callback_voice)
        rospy.Subscriber('/follow/point', NavGoalMsg, self.callback_follow)
        rospy.Subscriber('/base/base_pos', Pose2D, self.callback_base_position)

        self.delay = Delay()
        self.reconfig = Reconfig()
        self.robot_position = None
        self.location_list = {}
        read_location(self.location_list)
        self.state = 'init'

    def callback_door(self, data):
        self.main(Devices.door, data.data)

    def callback_base(self, data):
        self.main(Devices.base, data.data)

    def callback_manipulator(self, data):
        self.main(Devices.manipulator, data.data)

    def callback_voice(self, data):
        self.main(Devices.voice, data.data)

    def callback_follow(self, data):
        self.main(Devices.follow, data)

    def callback_base_position(self, data):
        self.robot_position = data

    def main(self, device, data):
        pass

    def move_robot(self, location):
        Publish.move_absolute(self.location_list[location].position)

    def speak(self, message):
        p = Popen(['espeak','-ven+f4',message,'-s 120'])

    def stop_robot():
        Publish.move_robot(NavGoalMsg('stop', 'absolute', Pose2D(0.0, 0.0, 0.0)))

if __name__ == '__main__':
    try:
        BaseState()
    except Exception, error:
        print str(error)
	
