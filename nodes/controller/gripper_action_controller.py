import rospy
import actionlib
from control_msgs.msg import GripperCommand, GripperCommandGoal, GripperCommandAction

__author__ = 'Nicole'


class GripperActionController:
    def __init__(self, gripper_side):
        # gripper_side should be right_gripper or left_gripper
        self.gripper_client = actionlib.SimpleActionClient('/dynamixel/' + gripper_side + '_controller/gripper_action',
                                                           GripperCommandAction)

    def open(self):
        action_open = GripperCommandGoal()
        action_open.command.position = 0.6
        self.gripper_client.send_goal(action_open)

    def close(self):
        action_close = GripperCommandGoal()
        action_close.command.position = 0.0
        self.gripper_client.send_goal(action_close)
