__author__ = 'nicole'

import rospy
from std_msgs.msg import String
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class Neck(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/pan/tilt/neck/state', String, self.callback_base_status)  # not sure

    def callback_base_status(self, data):
        self.broadcast(Devices.NECK, data)