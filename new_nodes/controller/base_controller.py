__author__ = "AThousandYears"

import rospy
import actionlib
from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_srvs.srv import Empty


class BaseController:
    def __init__(self):
        self.moveBase = actionlib.SimpleActionClient('/navigation/move_base', MoveBaseAction)
        self.clearCostmap = rospy.ServiceProxy('/navigation/move_base/clear_costmaps', Empty)

    def set_absolute_position(self, x, y, theta):
        rospy.loginfo("Move robot to " + str((x, y, theta)) + ' in map')
        self.set_new_goal(x, y, theta, 'map')

    def set_relative_position(self, x, y, theta):
        rospy.loginfo("Move robot to " + str((x, y, theta)) + ' from current pose')
        self.set_new_goal(x, y, theta, 'base_link')

    def set_new_goal(self, x, y, theta, frame_id):
        self.moveBase.cancel_goal()

        new_goal = MoveBaseGoal()

        new_goal.target_pose.header.frame_id = frame_id
        new_goal.target_pose.header.stamp = rospy.Time.now()

        new_goal.target_pose.pose.position.x = x
        new_goal.target_pose.pose.position.y = y

        quaternion = quaternion_from_euler(0, 0, theta)
        new_goal.target_pose.pose.orientation.z = quaternion[2]
        new_goal.target_pose.pose.orientation.w = quaternion[3]

        self.moveBase.send_goal(new_goal)

    def clear_costmaps(self):
        rospy.loginfo("Clear Costmaps")
        self.clearCostmap()
