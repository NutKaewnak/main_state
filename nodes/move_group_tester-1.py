#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
# from control_module import ManipulateController

group = None


def debugging_node():
    global group, manipulator_ctrl
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial')
    # manipulator_ctrl = ManipulateController()
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    rospy.sleep(1)
    print robot.get_group_names()
    group = moveit_commander.MoveGroupCommander("right_arm")
    rospy.sleep(1)
    manipulate("right_arm", [0.6, -0.15, 0.68])
    rospy.sleep(5)
    moveit_commander.roscpp_shutdown()
    print "ku ja shutdown la na"


def manipulate(arm_group, position, orientation_rpy=[0, 0, 0], tolerance=[0.05, 0.1], ref_frame="base_link",
                   planning_time=50.00):
    global group
    pose_target = geometry_msgs.msg.Pose()
    quaternion = tf.transformations.quaternion_from_euler(orientation_rpy[0], orientation_rpy[1], orientation_rpy[2])
    pose_target.position.x = position[0]
    pose_target.position.y = position[1]
    pose_target.position.z = position[2]
    pose_target.orientation.x = quaternion[0]
    pose_target.orientation.y = quaternion[1]
    pose_target.orientation.z = quaternion[2]
    pose_target.orientation.w = quaternion[3]

    if arm_group == "right_arm":
        group.set_planning_time(planning_time)
        group.clear_pose_targets()
        group.set_goal_position_tolerance(tolerance[0])
        group.set_goal_orientation_tolerance(tolerance[1])
        group.set_pose_reference_frame(ref_frame)
        group.set_pose_target(pose_target)
        group.go(False)  # async_move
    else:
        rospy.logwarn("No specified arm_group")


if __name__ == '__main__':
    try:
        debugging_node()
    except rospy.ROSInterruptException:
        pass