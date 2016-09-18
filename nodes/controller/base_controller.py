import rospy
import actionlib
from geometry_msgs.msg import Twist, PoseStamped
from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_srvs.srv import Empty
from athome_move_base.srv import ClearPointCostmap

__author__ = "AThousandYears"


class BaseController:
    def __init__(self):
        self.move_base = actionlib.SimpleActionClient('/navigation/move_base', MoveBaseAction)
        self.clear_costmap = rospy.ServiceProxy('/navigation/athome_move_base_node/clear_costmaps', Empty)
        self.clear_point_costmap = rospy.ServiceProxy('/navigation/athome_move_base_node/clear_point_costmaps', ClearPointCostmap)
        self.move_twist = rospy.Publisher('/base/cmd_vel', Twist, queue_size=1)
        self.goal_with_clear_point = rospy.Publisher('navigation/goal_with_clear_costmap', PoseStamped)
    #
    # def set_goal_with_clear_point(self, x, y, theta, frame_id):
    #     new_goal = PoseStamped()
    #     new_goal.header.frame_id = frame_id
    #     new_goal.header.stamp = rospy.Time.now()
    #
    #     new_goal.pose.position.x = x
    #     new_goal.pose.position.y = y
    #
    #     quaternion = quaternion_from_euler(0, 0, theta)
    #     new_goal.pose.orientation.z = quaternion[2]
    #     new_goal.pose.orientation.w = quaternion[3]
    #     # self.move_base.send_goal(new_goal)
    #     self.goal_with_clear_point(new_goal)

    def set_twist(self, twist):
        rospy.loginfo("Send Twist " + str((twist.linear.x, twist.linear.y, twist.angular.z)) + ' to robot.')
        self.move_twist.publish(twist)

    def set_twist_stop(self):
        stop_twist = Twist()
        self.move_twist.publish(stop_twist)

    def set_absolute_position(self, x, y, theta):
        rospy.loginfo("Move robot to " + str((x, y, theta)) + ' in map')
        self.move_base.cancel_goal()
        self.clear_costmaps()
        self.set_new_goal(x, y, theta, 'map')

    def set_relative_position(self, x, y, theta):
        rospy.loginfo("Move robot to " + str((x, y, theta)) + ' from current pose')
        self.move_base.cancel_goal()
        self.clear_costmaps()
        self.set_new_goal(x, y, theta, 'base_link')

    # def set_absolute_position_with_clear_point(self, x, y, theta):
    #     rospy.loginfo("Move robot to " + str((x, y, theta)) + ' in map')
        # self.move_base.cancel_goal()
        # self.clear_costmaps()
        # self.set_goal_with_clear_point(x, y, theta, 'map')

    # def set_relative_position_with_clear_point(self, x, y, theta):
    #     rospy.loginfo("Move robot to " + str((x, y, theta)) + ' from current pose')
        # self.move_base.cancel_goal()
        # self.clear_costmaps()
        # self.set_goal_with_clear_point(x, y, theta, 'base_link')

    def set_relative_position_without_clear_costmap(self, x, y, theta):
        rospy.loginfo("Move robot to " + str((x, y, theta)) + ' from current pose')

        self.set_new_goal(x, y, theta, 'base_link')

    def set_new_goal(self, x, y, theta, frame_id):

        new_goal = MoveBaseGoal()
        new_goal.target_pose.header.frame_id = frame_id
        new_goal.target_pose.header.stamp = rospy.Time.now()

        new_goal.target_pose.pose.position.x = x
        new_goal.target_pose.pose.position.y = y

        quaternion = quaternion_from_euler(0, 0, theta)
        new_goal.target_pose.pose.orientation.z = quaternion[2]
        new_goal.target_pose.pose.orientation.w = quaternion[3]
        self.move_base.send_goal(new_goal)

    def clear_costmaps(self):
        rospy.loginfo("Clear Costmaps")
        # self.clear_costmap()

    #Input frame_id: base_link
    def clear_point_costmaps(self, x, y, box_size):
        rospy.loginfo("Clear Point Costmaps")
        self.clear_point_costmap(x, y, box_size)


