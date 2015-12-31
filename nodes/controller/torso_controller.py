import rospy
from joint_trajectory_follow import JointTrajectoryFollow

__author__ = "AThousandYears"


class TorsoController:
    def __init__(self):
        self.torso = JointTrajectoryFollow('torso_controller', ['prismatic_joint'])

    def set_height_relative(self, height):
        rospy.loginfo("Set height to " + str(height))
        self.torso.move_joint([height])
