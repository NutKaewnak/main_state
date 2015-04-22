__author__ = "AThousandYears"

import rospy
from geometry_msgs.msg import Vector3


class NeckController:
    def __init__(self):
        self.set_neck_angle = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)

    def set_neck_angle(self, pitch, yaw):
        rospy.loginfo("Set neck to RPY" + str((0, pitch, yaw)))

        new_angle = Vector3()
        new_angle.y = pitch
        new_angle.z = yaw

        self.set_neck_angle.publish(new_angle)
