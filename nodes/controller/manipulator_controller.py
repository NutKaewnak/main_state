import rospy
import tf
from include.moveit_initiator import MoveItInitiator
from geometry_msgs.msg import PoseStamped, Pose, PointStamped
import math

__author__ = "your mum"

FIRST_SHELF = 1.40
SECOND_SHELF = 1.09
THIRD_SHELF = 0.70
FOURTH_SHELF = 0.35
FIFTH_SHELF = 0.10

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
        self.arm_group.set_planning_time(60)
        rospy.loginfo('Manipulator_controller init: ' + self.arm_side)

    def pick(self, object_pose, object_name='black_cock'):
        """

        :param object_pose: (PoseStamped)
        :param object_name: (str)
        :return:
        """
        self.remove_object(object_name)
        # if 'plane' not in self.world_object:
        #     pose_stamped = PoseStamped()
        #     pose_stamped.header.frame_id = '/odom_combined'
        #     pose_stamped.pose.position.z = 0.73
        #     self.scene.add_plane('plane', pose_stamped)
        # object_pose.pose.position.x += -0.10
        # object_pose.pose.position.y += 0.05
        # object_pose.pose.position.z += 0.05

        p = PoseStamped()
        p.header.frame_id = robot.get_planning_frame()
        p.pose.position.x = 0.75
        p.pose.position.y = 0.00
        p.pose.position.z = FIRST_SHELF
        scene.add_box("FIRST_SHELF", p, (0.33, 3.0, 0.05))
        rospy.sleep(1)

        p.pose.position.x = 0.75
        p.pose.position.y = 0.00
        p.pose.position.z = SECOND_SHELF
        scene.add_box("SECOND_SHELF", p, (0.33, 3.0, 0.05))
        rospy.sleep(1)

        p.pose.position.x = 0.75
        p.pose.position.y = 0.00
        p.pose.position.z = THIRD_SHELF
        scene.add_box("THIRD_SHELF", p, (0.33, 3.0, 0.05))
        rospy.sleep(1)

        p.pose.position.x = 0.75
        p.pose.position.y = 0.00
        p.pose.position.z = FOURTH_SHELF
        scene.add_box("FOURTH_SHELF", p, (0.33, 3.0, 0.05))
        rospy.sleep(1)

        p.pose.position.x = 0.75
        p.pose.position.y = 0.00
        p.pose.position.z = FIFTH_SHELF
        scene.add_box("FIFTH_SHELF", p, (0.33, 3.0, 0.05))
        rospy.sleep(1)

        self.scene.add_box(object_name, object_pose, (0.05, 0.05, 0.05))
        self.world_object.append(object_name)
        result = self.arm_group.pick(object_name)
        print 'picking:', object_name
        print result
        return result

    def static_pose(self, pose_name):
        """

        :param pose_name: (str) eg. right_normal
        :return: (None)
        """
        self.arm_group.set_named_target(pose_name)
        self.arm_group.go()

    def remove_object(self, object_name):
        self.scene.remove_world_object(object_name)
        if object_name in self.world_object:
            self.world_object.remove(object_name)
            rospy.loginfo("Remove " + str(object_name) + " from world.")
        else:
            rospy.loginfo("No such " + str(object_name) + " in world.")

    def remove_all_object(self):
        for object_name in self.world_object:
            self.remove_object(object_name)
