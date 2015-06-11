__author__ = 'nicole'

import rospy
from dynamixel_msgs.msg import JointState
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class Neck(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/dynamixel/pan_controller/state', JointState, self.callback_pan_status)
        rospy.Subscriber('/dynamixel/tilt_controller/state', JointState, self.callback_tilt_status)
        self.neck_status = NeckStatus()

    def callback_pan_status(self, data):
        self.neck_status.pan = data.current_pos
        self.broadcast(Devices.NECK, self.neck_status)

    def callback_tilt_status(self, data):
        self.neck_status.tilt = data.current_pos
        self.broadcast(Devices.NECK, self.neck_status)


class NeckStatus:
    def __init__(self):
        self.tilt = None
        self.pan = None