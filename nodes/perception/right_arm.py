import rospy
from control_msgs.msg import FollowJointTrajectoryActionResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'Nicole'


class RightArm(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/dynamixel/right_arm_controller/follow_joint_trajectory/result',
                         FollowJointTrajectoryActionResult, self.callback_arm_status)

    def callback_arm_status(self, data):
        self.broadcast(Devices.RIGHT_ARM, data.status.status)
