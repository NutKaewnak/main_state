__author__ = 'Nicole'

import rospy
from dynamixel_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryActionResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class Height(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        self.height_data = HeightData()
        rospy.Subscriber('/dynamixel/torso_controller/state', JointState, self.callback_position)
        rospy.Subscriber('/dynamixel/torso_controller/follow_joint_trajectory/result',
                         FollowJointTrajectoryActionResult, self.callback_status)

    def callback_position(self, data):
        self.height_data.pos = data.actual.positions[0]  # 0.02 0.2
        self.broadcast(Devices.NECK, self.height_data)

    def callback_status(self, data):
        self.height_data.status = data.status.status
        self.broadcast(Devices.NECK, self.height_data)


class HeightData:
    def __init__(self):
        self.pos = None
        self.status = None

        # Don't forget to add this perception into perception_module