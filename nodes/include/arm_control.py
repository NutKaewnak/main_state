import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import GripperCommandAction, GripperCommandGoal


class RightArm:
    def __init__(self):
        self.ra = actionlib.SimpleActionClient('/dynamixel/right_arm_controller/follow_joint_trajectory',
                                                FollowJointTrajectoryAction)
        self.rg = actionlib.SimpleActionClient('/dynamixel/right_gripper_controller/gripper_action',
                                               GripperCommandAction)
        rospy.loginfo('Waiting for joint trajectory action')
        self.ra.wait_for_server()
        self.rg.wait_for_server()
        rospy.loginfo('Found joint trajectory action!')

    def move_right_joint(self, angles):
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ['right_shoulder_1_joint',
                                       'right_shoulder_2_joint',
                                       'right_elbow_joint',
                                       'right_wrist_1_joint',
                                       'right_wrist_2_joint',
                                       'right_wrist_3_joint']
        point = JointTrajectoryPoint()
        point.positions = angles
        point.time_from_start = rospy.Duration(1)

        goal.trajectory.points.append(point)
        self.ra.send_goal(goal)

    def open(self):
        action_open = GripperCommandGoal()
        action_open.command.position = 0.6
        self.rg.send_goal(action_open)
        self.rg.wait_for_result()
        if self.rg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')

    def close(self):
        action_close = GripperCommandGoal()
        action_close.command.position = 0
        self.rg.send_goal(action_close)
        self.rg.wait_for_result()
        if self.rg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')


class LeftArm:
    def __init__(self):
        self.la = actionlib.SimpleActionClient('/dynamixel/left_arm_controller/follow_joint_trajectory',
                                               FollowJointTrajectoryAction)
        self.lg = actionlib.SimpleActionClient('/dynamixel/left_gripper_controller/gripper_action',
                                               GripperCommandAction)
        rospy.loginfo('Waiting for joint trajectory action')
        self.la.wait_for_server()
        rospy.loginfo('Found joint trajectory action!')
        self.lg.wait_for_server()
        rospy.loginfo('Found joint trajectory action!')

    def move_left_joint(self, angles):
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ['left_shoulder_1_joint',
                                       'left_shoulder_2_joint',
                                       'left_elbow_joint',
                                       'left_wrist_1_joint',
                                       'left_wrist_2_joint',
                                       'left_wrist_3_joint']

        point = JointTrajectoryPoint()
        point.positions = angles
        point.time_from_start = rospy.Duration(1)

        goal.trajectory.points.append(point)
        self.la.send_goal(goal)

    def open(self):
        action_open = GripperCommandGoal()
        action_open.command.position = 0.6
        self.lg.send_goal(action_open)
        self.lg.wait_for_result()
        if self.lg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')

    def close(self):
        action_close = GripperCommandGoal()
        action_close.command.position = 0.0
        self.lg.send_goal(action_close)
        self.lg.wait_for_result()
        if self.lg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')

