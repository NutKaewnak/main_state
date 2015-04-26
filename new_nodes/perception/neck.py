__author__ = 'nicole'

import rospy
from std_msgs.msg import String
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class Neck(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/pan_kinect/state', String, self.callback_neck_status)
        rospy.Subscriber('/tilt_kinect/state', String, self.callback_neck_status)

    def callback_neck_status(self, data):
        self.broadcast(Devices.NECK, data)