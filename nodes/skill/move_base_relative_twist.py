import math
from geometry_msgs.msg import Pose2D, Twist
from include.delay import Delay
from include.abstract_skill import AbstractSkill

__author__ = "nicole"

VEL_LINEAR_X = 0.3
VEL_LINEAR_Y = 0.05
VEL_ANGULAR_Z = 0.1


class MoveBaseRelativeTwist(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.is_active = False
        self.timer_linear = Delay()
        self.timer_angular = Delay()
        self.goal_pose_2d = Pose2D()
        self.is_performing = False
        self.current_twist = Twist()

    def stop(self):
        self.change_state('stop')
        self.controlModule.base.set_twist_stop()

    def set_position(self, dx, dy, dtheta):
        self.change_state('active')
        self.goal_pose_2d = Pose2D()
        self.goal_pose_2d.x = dx
        self.goal_pose_2d.y = dy
        self.goal_pose_2d.theta = dtheta

    def cal_wait_time(self, goal_pose2d, twist):
        t_linear = 0
        t_angular = 0
        if math.hypot(twist.linear.x, twist.linear.y):
            t_linear = math.hypot(goal_pose2d.x, goal_pose2d.y) / math.hypot(twist.linear.x, twist.linear.y)
            t_linear *= 1.05
        if twist.angular.z:
            t_angular = goal_pose2d.theta / twist.angular.z
            t_angular *= 0.92

        self.timer_angular = t_angular
        self.timer_linear = t_linear

    def perform(self, perception_data):
        if self.is_performing:
            return
        else:
            self.is_performing = True

        if not self.timer_angular.is_waiting():
            twist = self.current_twist
            self.current_twist = Twist()
            self.current_twist.linear = twist.linear
            self.controlModule.base.set_twist(twist)

        if not self.timer_linear.is_waiting():
            twist = self.current_twist
            self.current_twist = Twist()
            self.current_twist.angular = twist.angular
            self.controlModule.base.set_twist(twist)

        if self.state is 'active':
            twist = Twist()
            if self.goal_pose_2d.x and self.goal_pose_2d.y:
                goal_temp = Pose2D()
                goal_temp.theta = math.atan2(self.goal_pose_2d.y, self.goal_pose_2d.x)
                if goal_temp.theta > 0:
                    twist.angular.z = VEL_ANGULAR_Z
                elif goal_temp.theta < 0:
                    twist.angular.z = -1 * VEL_ANGULAR_Z

                twist.linear.x = VEL_LINEAR_X
                self.goal_pose_2d.theta -= goal_temp.theta

                self.cal_wait_time(goal_temp, twist)

                self.current_twist = twist
                self.controlModule.base.set_twist(self.current_twist)
                self.change_state('send_xy_goal')
            else:
                if self.goal_pose_2d.x > 0:
                    twist.linear.x = VEL_LINEAR_X
                elif self.goal_pose_2d.x < 0:
                    twist.linear.x = -1 * VEL_LINEAR_X

                elif self.goal_pose_2d.y > 0:
                    twist.linear.y = VEL_LINEAR_Y
                elif self.goal_pose_2d.y < 0:
                    twist.linear.y = -1 * VEL_LINEAR_Y

                self.cal_wait_time(self.goal_pose_2d, twist)
                self.current_twist = twist
                self.controlModule.base.set_twist(self.current_twist)
                self.change_state('send_xy_goal')

        elif self.state is 'send_xy_goal':
            if not self.timer_linear.is_waiting() and not self.timer_angular.is_waiting():
                twist = Twist()
                if self.goal_pose_2d.theta > 0:
                    twist.angular.z = VEL_ANGULAR_Z
                elif self.goal_pose_2d.theta < 0:
                    twist.angular.z = -1 * VEL_ANGULAR_Z
                self.cal_wait_time(self.goal_pose_2d, twist)
                self.controlModule.base.set_twist(twist)
                self.change_state('send_theta_goal')

        elif self.state is 'send_theta_goal':
            if not self.timer_linear.is_waiting() and not self.timer_angular.is_waiting():
                self.controlModule.base.set_twist_stop()
                self.change_state('succeeded')

        self.is_performing = False
