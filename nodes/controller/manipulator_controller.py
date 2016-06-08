import rospy
import tf
from include.moveit_initiator import MoveItInitiator
from geometry_msgs.msg import PoseStamped, Pose, PointStamped
import math

__author__ = "ftprainnie"

REFERENCE_FRAME = 'base_link'


class ManipulateController:
    def __init__(self, arm_side='right_arm'):
        """

        :param arm_side: (string) should be either 'left_arm' or 'right_arm'
        :return: (None)
        """
        self.arm_side = arm_side
        self.arm_group = None
        self.robot = None
        self.scene = None
        self.tf_listener = None
        self.moveit_initiator = None
        self.world_object = []

    def init_controller(self):
        self.moveit_initiator = MoveItInitiator()
        self.robot = self.moveit_initiator.robot
        self.scene = self.moveit_initiator.scene
        self.tf_listener = self.moveit_initiator.tf_listener
        self.arm_group = self.moveit_initiator.init_controller(self.arm_side)
        self.arm_group.set_planning_time(100)
        rospy.loginfo('Manipulator_controller init:', self.arm_side)

    def pick(self, object_pose, object_name='black_cock'):
        """

        :param object_pose: (PoseStamped)
        :param object_name: (str)
        :return:
        """
        self.scene.add_sphere(object_name, object_pose, 0.05)
        self.world_object.append(object_name)
        self.arm_group.pick(object_pose)

    def static_pose(self, pose_name):
        """

        :param pose_name: (str) eg. right_normal
        :return: (None)
        """
        self.arm_group.set_named_target(pose_name)
        self.arm_group.go()

    def remove_object(self, object_name):
        self.scene.remove_world_object(object_name)
        self.world_object.remove(object_name)

    def remove_all_object(self):
        for object_name in self.world_object:
            self.remove_object(object_name)
