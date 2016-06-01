import rospy
from joint_trajectory_follow import JointTrajectoryFollow
from dynamixel_controllers.srv import SetTorqueLimit

__author__ = 'Nicole'

GRIPPER_EFFORT = 0.0


class GripperController:
    def __init__(self):
        self.gripper_motor = JointTrajectoryFollow('right_gripper_controller', ['right_gripper_joint'])
        self.set_torque_limit = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit',
                                                   SetTorqueLimit)

    def gripper_open(self, gripper_effort=GRIPPER_EFFORT):
        self.set_torque_limit(gripper_effort)
        self.gripper_motor.move_joint(0.5)

    def gripper_close(self, gripper_effort=GRIPPER_EFFORT):
        self.set_torque_limit(gripper_effort)
        self.gripper_motor.move_joint(0.0)
