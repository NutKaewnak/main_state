__author__ = "AThousandYears"

import rospy
from geometry_msgs.msg import Vector3


class NeckController:
    def __init__(self):
        self.set_neck_angle_topic = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)

    def set_neck_angle(self, pitch, yaw):
        rospy.loginfo("Set neck to RPY" + str((pitch, yaw)))

        new_angle = Vector3()
        new_angle.x = 0
        new_angle.y = pitch
        new_angle.z = yaw

        self.set_neck_angle_topic.publish(new_angle)
