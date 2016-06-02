import rospy
import actionlib
from control_msgs.msg import GripperCommandGoal, GripperCommandAction
from dynamixel_controllers.srv import SetTorqueLimit

__author__ = 'Nicole'

GRIPPER_EFFORT = 0.0


class GripperActionController:
    def __init__(self, gripper_side):
        # gripper_side should be right_gripper or left_gripper
        self.gripper_client = actionlib.SimpleActionClient('/dynamixel/' + gripper_side + '_controller/gripper_action',
                                                           GripperCommandAction)
        self.set_torque_limit = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit',
                                                   SetTorqueLimit)

    def gripper_open(self, gripper_effort=GRIPPER_EFFORT):
        action_open = GripperCommandGoal()
        action_open.command.position = 0.6
        self.set_torque_limit(gripper_effort)
        self.gripper_client.send_goal(action_open)

    def gripper_close(self, gripper_effort=GRIPPER_EFFORT):
        action_close = GripperCommandGoal()
        action_close.command.position = 0.0
        self.set_torque_limit(gripper_effort)
        self.gripper_client.send_goal(action_close)
