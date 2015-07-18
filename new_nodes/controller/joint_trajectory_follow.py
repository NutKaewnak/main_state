__author__ = 'Nicole'

import rospy
import actionlib
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal


class JointTrajectoryFollow:
    def __init__(self, motor_name, joint_names):
        # arm_name should be b_arm or f_arm
        self.name = motor_name
        self.joint_names = joint_names
        self.jta = actionlib.SimpleActionClient('/dynamixel/'+self.name+'/follow_joint_trajectory'
                                                , FollowJointTrajectoryAction)
        # rospy.loginfo('Waiting for joint trajectory action')
        # self.jta.wait_for_server()
        # rospy.loginfo('Found joint trajectory action!')

    def move_joint(self, angles):
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = self.joint_names
        rospy.loginfo('send: ' + str(angles) + ' to ' + str(self.joint_names))
        point = JointTrajectoryPoint()
        point.positions = angles
        point.time_from_start = rospy.Duration(3)
        goal.trajectory.points.append(point)
        self.jta.send_goal(goal)
