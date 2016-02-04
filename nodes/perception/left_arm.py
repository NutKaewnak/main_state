import rospy
from control_msgs.msg import FollowJointTrajectoryActionResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'Nicole'


class LeftArm(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/dynamixel/left_arm_controller/follow_joint_trajectory/result',
                         FollowJointTrajectoryActionResult, self.callback_arm_status)

    def callback_arm_status(self, data):
        self.broadcast(Devices.LEFT_ARM, data.status.status)

    # Don't forget to add this perception into perception_module
