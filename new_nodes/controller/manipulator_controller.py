__author__ = "kandithws"

import rospy
import moveit_commander
import moveit_msgs.msg
import std_msgs.msg
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import tf


class ManipulateController:
    def __init__(self):
        # group should be "left_arm" or "right_arm"
        # self.moveit_commander.roscpp_initialize(" ")
        moveit_commander.roscpp_initialize(" ")
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.grasp_plan = None

        # self.group = self.moveit_commander.MoveGroupCommander(arm_group)
        # self.group.set_planning_time(planning_time)

    def __del__(self):
        # Deconstructor should be call before shutdown nodes
        moveit_commander.roscpp_shutdown()

    def manipulate(self, arm_group, position, orientation_rpy=[0, 0, 0], ref_frame="base_link", planning_time=30.00):
        pose_target = geometry_msgs.msg.Pose()
        quaternion = tf.transformations.quaternion_from_euler(orientation_rpy[0],
                                                              orientation_rpy[1],
                                                              orientation_rpy[2])
        pose_target.orientation.x = quaternion[0]
        pose_target.orientation.y = quaternion[1]
        pose_target.orientation.z = quaternion[2]
        pose_target.orientation.w = quaternion[3]
        pose_target.position.x = position[0]
        pose_target.position.y = position[1]
        pose_target.position.z = position[2]

        if arm_group is "right_arm":
            self.robot.right_arm.set_planning_time(planning_time)
            self.robot.right_arm.clear_pose_targets()
            self.robot.right_arm.set_pose_reference_frame(ref_frame)
            self.robot.right_arm.set_pose_target(pose_target)
            self.robot.right_arm.go(False)  # async_move

        elif arm_group is "left_arm":
            self.robot.left_arm.set_planning_time(planning_time)
            self.robot.left_arm.clear_pose_targets()
            self.robot.left_arm.set_pose_reference_frame(ref_frame)
            self.robot.left_arm.set_pose_target(pose_target)
            self.robot.left_arm.go(False)  # async_move
        else:
            rospy.logwarn("No specified arm_group")

    def change_grasp_plan_constraint(self, plan_id):
        self.grasp_plan = plan_id

    def pick(self, arm_group, position, desired_object="part", support_surface_name="table", orientation_rpy=[0, 0, 0],
             ref_frame="base_link", planning_time=50.00, grasp_constraint=None):

        pose_target = geometry_msgs.msg.PoseStamped()

        pose_target.header.frame_id = ref_frame
        quaternion = tf.transformations.quaternion_from_euler(orientation_rpy[0], orientation_rpy[1],
                                                              orientation_rpy[2])
        pose_target.pose.orientation.x = quaternion[0]
        pose_target.pose.orientation.y = quaternion[1]
        pose_target.pose.orientation.z = quaternion[2]
        pose_target.pose.orientation.w = quaternion[3]
        pose_target.pose.position.x = position[0]
        pose_target.pose.position.y = position[1]
        pose_target.pose.position.z = position[2]

        if grasp_constraint is None:
            grasp_constraint = moveit_msgs.msg.Grasp()
            grasp_constraint.grasp_pose = pose_target

            grasp_constraint.pre_grasp_approach.direction.vector.x = 1.0
            grasp_constraint.pre_grasp_approach.direction.header.frame_id = "right_wrist_3_Link"
            grasp_constraint.pre_grasp_approach.min_distance = 0.05
            grasp_constraint.pre_grasp_approach.desired_distance = 0.3

            # Retreat directly move_back
            grasp_constraint.post_grasp_retreat.direction.header.frame_id = "base_link"
            grasp_constraint.post_grasp_retreat.direction.vector.x = -1.0
            grasp_constraint.post_grasp_retreat.min_distance = 0.05
            grasp_constraint.post_grasp_retreat.desired_distance = 0.2

            # open_gripper
            grasp_constraint.pre_grasp_posture.joint_names.append("right_gripper_joint")
            grasp_constraint.pre_grasp_posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
            grasp_constraint.pre_grasp_posture.points[0].positions.append(std_msgs.msg.Float64())
            grasp_constraint.pre_grasp_posture.points[0].positions[0] = 1

            # close_gripper
            grasp_constraint.grasp_posture.joint_names.append("right_gripper_joint")
            grasp_constraint.grasp_posture.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
            grasp_constraint.grasp_posture.points[0].positions.append(std_msgs.msg.Float64())
            grasp_constraint.grasp_posture.points[0].positions[0] = 0.4

            grasp = [grasp_constraint]

        if arm_group is "right_arm":
            self.robot.right_arm.set_support_surface_name(support_surface_name)
            self.robot.right_arm.set_planning_time(planning_time)
            self.robot.right_arm.pick(desired_object, grasp)
        elif arm_group is "left_arm":
            self.robot.left_arm.set_support_surface_name(support_surface_name)
            self.robot.left_arm.set_planning_time(planning_time)
            self.robot.left_arm.pick(desired_object, grasp)
        else:
            rospy.logwarn("No specified arm_group")