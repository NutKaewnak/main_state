__author__ = 'nicole'

import rospy
from dynamixel_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryActionResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class Neck(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/dynamixel/pan_controller/state', JointState, self.callback_pan_status)
        rospy.Subscriber('/dynamixel/tilt_controller/state', JointState, self.callback_tilt_status)
        rospy.Subscriber('/dynamixel/neck_controller/follow_joint_trajectory/result',
                         FollowJointTrajectoryActionResult, self.callback_status)
        self.neck_pos = NeckPos

    def callback_pan_status(self, data):
        self.neck_pos.pan = data.current_pos
        self.broadcast(Devices.NECK, self.neck_pos)

    def callback_tilt_status(self, data):
        self.neck_pos.tilt = data.current_pos
        self.broadcast(Devices.NECK, self.neck_pos)

    def callback_status(self, data):
        self.neck_pos.status = data.status.status


class NeckPos:
    def __init__(self):
        self.tilt = None
        self.pan = None
        self.result = None