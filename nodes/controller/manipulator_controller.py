import rospy
import tf
from include.moveit_initiator import MoveItInitiator
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import PointStamped
from skill.include import inverse_kinematics


__author__ = "ftprainnie"

GRIPPER_OPENED = 0.8
GRIPPER_CLOSED = 0.0
GRIPPER_NEUTRAL = 0.0
GRASP_OVERTIGHTEN = -0.01

REFERENCE_FRAME = 'base_link'


class ManipulateController:
    def __init__(self, arm_side='right_arm'):
        """

        :param arm_side: (string) should be either 'left_arm' or 'right_arm'
        :return: (None)
        """
        self.arm_side = arm_side
        self.arm_group = None
        self.set_torque_limit = {}
        self.robot = None
        self.scene = None
        self.tf_listener = None
        self.moveit_initiator = None
        self.obj_pos = None

    def init_controller(self):
        self.moveit_initiator = MoveItInitiator()
        self.robot = self.moveit_initiator.robot
        self.scene = self.moveit_initiator.scene
        self.tf_listener = self.moveit_initiator.tf_listener
        self.arm_group = self.moveit_initiator.init_controller(self.arm_side)

    def init_position(self, point):
        """
        Init position and flip y-axis for invert kinematic
        :param point: (geometry/Point)
        :return: None
        """
        rospy.loginfo("-----INVK INIT POSITION-----")
        if self.arm_group == 'right_arm':
            pass
        elif self.arm_group == 'left_arm':
            point.y *= -1
        self.obj_pos = point

    def transform_point(self, pos, origin_frame='base_link'):
        """
        Transform point from origin frame (Default: 'base_link') to 'mani_link'
        :param pos: (geometry_msgs.msg.PointStamped)
        :param origin_frame:
        :return: (geometry_msgs.msg.PointStamped), False if input arm_group is incorrect
        """
        # destination_frame = None
        # if 'ARM' in arm_group or 'arm' in arm_group:
        # destination_frame = "torso_Link"
        # destination_frame = "right_mani_link"
        if "right" in self.arm_side:
            destination_frame = "right_mani_link"
        elif "left" in self.arm_side:
            destination_frame = "left_mani_link"
        tf_points = PointStamped()
        tf_points.point.x = pos.x
        tf_points.point.y = pos.y
        tf_points.point.z = pos.z
        tf_points.header.stamp = rospy.Time(0)
        tf_points.header.frame_id = origin_frame
        print "Waiting For Transform"
        self.tf_listener.waitForTransform(destination_frame, origin_frame, rospy.Time(0), rospy.Duration(4.00))
        print "Success Waiting"
        point_out = self.tf_listener.transformPoint(destination_frame, tf_points)
        print 'HERRREEEE >>>>> ' + str(point_out.point.x) + ', ' + str(point_out.point.y) + ', ' + str(point_out.point.z)
        return point_out.point

    def manipulate(self, pose_target, orientation_rpy=[0, 0, 0], ref_frame="base_link", planning_time=50.00):
        self.arm_group.set_planning_time(planning_time)
        self.arm_group.clear_pose_targets()
        self.arm_group.set_goal_position_tolerance(0.05)
        self.arm_group.set_goal_orientation_tolerance(0.1)
        self.arm_group.set_pose_reference_frame(ref_frame)
        self.arm_group.set_pose_target(pose_target)
        self.arm_group.go(False)  # async_move

    def get_joint_status(self):
        joint_state = {}
        group_joint_names = None
        group_current_joint_values = None
        group_joint_names = self.arm_group.get_joints()
        group_current_joint_values = self.arm_group.get_current_joint_values()
        for i in range(0, len(group_joint_names)):
            joint_state[group_joint_names[i]] = group_current_joint_values[i]
        return joint_state

    def move_relative(self, relative_goal_translation, relative_goal_rotation):
        # respect to efflink
        last_pose = self.arm_group.get_current_pose()
        rospy.loginfo(str(type(last_pose)) + '\n' + str(last_pose))

        rpy = tf.transformations.euler_from_quaternion([last_pose.pose.orientation.x,
                                                        last_pose.pose.orientation.y,
                                                        last_pose.pose.orientation.z,
                                                        last_pose.pose.orientation.w])

        new_pose = Pose()
        new_pose.position.x = last_pose.pose.position.x + relative_goal_translation[0]
        new_pose.position.y = last_pose.pose.position.y + relative_goal_translation[1]
        new_pose.position.z = last_pose.pose.position.z + relative_goal_translation[2]
        new_pose.orientation.x = rpy[0] + relative_goal_rotation[0]
        new_pose.orientation.y = rpy[1] + relative_goal_rotation[1]
        new_pose.orientation.z = rpy[2] + relative_goal_rotation[2]

        self.manipulate(new_pose)

    def move_joint(self, joint_name, joint_value):
        print joint_name
        print joint_value
        print self.arm_side
        print self.arm_group
        if (type(joint_name) == str) and (type(joint_value) == float):
            self.arm_group.clear_pose_targets()
            self.arm_group.set_joint_value_target(joint_name, joint_value)
            self.arm_group.go(False)
        else:
            rospy.logwarn("Invalid Argument")
            return False
        return True

    # PICKING PROCEDURE pregrasp -> open_gripper -> reach -> grasp
    def move_arm_group(self, angles):
        """
        Move array of arm joints with specific angle.
        :param angles: (dict()) dict of angle and arm_joint
        :return: (None)
        """
        for x in angles:
            if x in self.arm_group.get_joints():
                self.move_joint(x, angles[x])

    def static_pose(self, posture, tolerance=[0.05, 0.1]):
        self.arm_group.clear_pose_targets()
        self.arm_group.set_goal_position_tolerance(tolerance[0])
        self.arm_group.set_goal_orientation_tolerance(tolerance[1])
        self.arm_group.set_named_target(posture)
        self.arm_group.go(False)  # async_move

    def move_arm_pick_object_first(self):
        """
        Move arm to object position : x - 25 cm
        :param (none)
        :return: (none)
        """
        self.obj_pos.x -= 0.25
        angle = inverse_kinematics.inverse_kinematic(self.transform_point(self.obj_pos), 0)
        self.move_arm_pick(angle)

    def move_arm_pick_object_second(self):
        """
        Move arm to object position
        :param (none)
        :return: (None)
        """
        self.obj_pos.x += 0.1
        angle = inverse_kinematics.inverse_kinematic(self.transform_point(self.obj_pos), 0)
        self.move_arm_pick(angle)

    def move_arm_pick(self, angle):
        """
        Move arm joints with specific angle.
        :param angle: (dict()) dict of angle and arm_joint
        :return: (None)
        """
        self.move_joint('right_shoulder_1_joint', inverse_kinematics.in_bound('right_shoulder_1_joint', angle['right_shoulder_1_joint']))
        self.move_joint('right_shoulder_2_joint', inverse_kinematics.in_bound('right_shoulder_2_joint', angle['right_shoulder_2_joint']))
        self.move_joint('right_elbow_joint', inverse_kinematics.in_bound('right_elbow_joint', angle['right_elbow_joint']))
        self.move_joint('right_wrist_1_joint', inverse_kinematics.in_bound('right_wrist_1_joint', angle['right_wrist_1_joint']))
        self.move_joint('right_wrist_2_joint', inverse_kinematics.in_bound('right_wrist_2_joint', angle['right_wrist_2_joint']))
        self.move_joint('right_wrist_3_joint', inverse_kinematics.in_bound('right_wrist_3_joint', angle['right_wrist_3_joint']))

    def move_arm_before_pick_cloth(self):
        """
        Move arm joints with specific angle.
        :param angle: (dict()) dict of angle and arm_joint
        :return: (None)
        """
        self.obj_pos.z += 0.08
        angle = inverse_kinematics.inverse_kinematic(self.transform_point(self.obj_pos), 0.5*math.pi)
        self.move_arm_pick(angle)

    def move_arm_after_pick_cloth(self):
        self.static_pose('right_after_pick_cloth')