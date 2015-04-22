__author__ = "AThousandYears"

import rospy
from geometry_msgs.msg import PoseStamped


class BaseController:
    def __init__(self):
        self.set_position_topics = rospy.Publisher('/navigation/set_position', PoseStamped)

    def set_position(self, x, y, theta):
        rospy.loginfo("Move robot to " + str((x, y)))

        new_pose = PoseStamped()
        new_pose.pose.position.x = x
        new_pose.pose.position.y = y
        new_pose.pose.orientation.z = theta

        self.set_position_topics.publish(new_pose)
