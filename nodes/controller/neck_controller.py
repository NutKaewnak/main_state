from joint_trajectory_follow import JointTrajectoryFollow
# from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryGoal
import rospy
import actionlib

__author__ = "AThousandYears"


class NeckController:
    def __init__(self):
        self.neck_motor = JointTrajectoryFollow('neck_controller', ['tilt_joint', 'pan_joint'])
        # self.neck = actionlib.SimpleActionClient('/dynamixel/neck_controller/state', FollowJointTrajectoryAction)

    def set_neck_angle(self, pitch, yaw):
        self.neck_motor.move_joint([pitch, yaw])

    # def set_new_goal(self, pitch, yaw, frame_id):
    #
    #     new_goal = FollowJointTrajectoryGoal()
    #     print 'new_goal =' +str(new_goal)
    #     new_goal.trajectory.header.frame_id = frame_id
    #     new_goal.trajectory.header.stamp = rospy.Time.now()
    #
    #
    #     self.neck.send_goal(new_goal)
