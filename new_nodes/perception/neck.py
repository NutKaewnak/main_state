__author__ = 'nicole'

import rospy
from dynamixel_msgs.msg import JointState
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class Neck(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/dynamixel/pan_kinect/state', JointState, self.callback_pan_status)
        rospy.Subscriber('/dynamixel/tilt_kinect/state', JointState, self.callback_tilt_status)

    def callback_pan_status(self, data):
        self.pan = data.current_pos
        self.broadcast(Devices.NECK, data)

    def callback_tilt_status(self, data):
        self.tilt = data.current_pos
        self.broadcast(Devices.NECK, data)
