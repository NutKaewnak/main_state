import rospy
from control_msgs.msg import GripperCommandActionResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'Nicole'


class RightGripper(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/dynamixel/right_gripper_controller/gripper_action/result',
                         GripperCommandActionResult, self.callback_arm_status)

    def callback_arm_status(self, data):
        self.broadcast(Devices.RIGHT_GRIPPER, data.status.status)
