import rospy
from joint_trajectory_follow import JointTrajectoryFollow

__author__ = "AThousandYears"


class ArmController:
    def __init__(self, side):
        self.arm = JointTrajectoryFollow(side + '_arm_controller', [side + '_shoulder_1_joint',
                                                                    side + '_shoulder_2_joint',
                                                                    side + '_elbow_joint',
                                                                    side + '_wrist_1_joint',
                                                                    side + '_wrist_2_joint',
                                                                    side + '_wrist_3_joint'])

    def set_position(self, x, y, z):
        rospy.loginfo("Move " + self.side + " robot to " + str((x, y, z)))
        self.arm.move_joint([x, y, z])

    def set_action(self, action):
        rospy.loginfo("Set " + self.side + " robot to " + str(action))
        # not finished
