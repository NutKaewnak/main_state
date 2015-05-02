__author__ = "AThousandYears"

import rospy
from std_msgs.msg import Float64


class TorsoController:
    def __init__(self):
        self.set_height = rospy.Publisher('/hardware_bridge/set_height', Float64)

    def set_height(self, height):
        rospy.loginfo("Set height to " + str(height))

        self.set_height.publish(Float64(height))
