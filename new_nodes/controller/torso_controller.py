__author__ = "AThousandYears"

import rospy
from joint import Joint


class TorsoController:
    def __init__(self):
        self.torso = Joint('torso_controller', ['prismatic_joint'])

    def set_height_relative(self, height):
        rospy.loginfo("Set height to " + str(height))
        self.torso.move_joint(height)
