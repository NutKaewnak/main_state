import rospy
# from std_msgs.msg import String
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Path
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'CinDy'


class Navigate(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        # rospy.Subscriber('/base/status', String, self.callback_base_status)
        rospy.Subscriber("/navigate/move_base_node/TrajectoryPlannerROS/local_plan", Path, self.callback_local_plan)
        # rospy.Subscriber("/navigation/move_base_node/TrajectoryPlannerROS/global_plan", Path, self.callback_global_plan)
        self.position = (0, 0, 0)
        self.global_path = []
        # self.local_path = []

    # def callback_local_plan(self, data):
    #     self.broadcast(Devices.NAVIGATE, data)
    #     position = data.feedback.base_pos.poses.pose.position
    #     orientation = data.feedback.base_position.poses.pose.orientation
    #     quaternion = (0, 0, orientation.z, orientation.w)
    #     rpy_angle = euler_from_quaternion(quaternion)
    #     self.position = (position.x, position.y, rpy_angle[2])
    #     self.local_path = data.feedback.base_pos.poses.pose.position
    def callback_global_plan(self, data):
        self.broadcast(Devices.NAVIGATE, data)
        position = data.poses.pose.position
        orientation = data.poses.pose.orientation
        quaternion = (0, 0, orientation.z, orientation.w)
        rpy_angle = euler_from_quaternion(quaternion)
        self.position = (position.x, position.y, rpy_angle[2])
        self.global_path = data.poses

