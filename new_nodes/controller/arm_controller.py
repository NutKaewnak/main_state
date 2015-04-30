__author__ = "AThousandYears"

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Vector3


class ArmController:
    def __init__(self, side):
        self.side = side
        self.set_position_topics = rospy.Publisher('/manipulator/' + side + '/set_position', Vector3)
        self.set_action_topics = rospy.Publisher('/manipulator/' + side + '/set_action', String)

    def set_position(self, x, y, z):
        rospy.loginfo("Move " + self.side + " robot to " + str((x, y, z)))

        new_pose = Vector3()
        new_pose.x = x
        new_pose.y = y
        new_pose.z = z

        self.set_position_topics.publish(new_pose)

    def set_action(self, action):
        rospy.loginfo("Set " + self.side + " robot to " + str(action))

        self.set_action_topics.publish(String(action))