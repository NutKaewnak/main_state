import math
from geometry_msgs.msg import Pose2D, Twist
from include.delay import Delay
from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "nicole"


class MoveBaseRelativeTwist(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.is_active = False
        self.timer = Delay()
        self.goal_pose_2d = Pose2D()
        self.is_performing = False

    def stop(self):
        self.change_state('stop')
        self.controlModule.base.set_twist_stop()

    def set_position(self, dx, dy, dtheta):
        self.change_state('active')
        self.goal_pose_2d = Pose2D()
        self.goal_pose_2d.x = dx
        self.goal_pose_2d.y = dy
        self.goal_pose_2d.theta = dtheta

    def perform(self, perception_data):
        if self.is_performing:
            return
        else:
            self.is_performing = True

        if self.state is 'active':
            twist = Twist()
            if self.goal_pose_2d.x and self.goal_pose_2d.y:
                goal_temp = Pose2D()
                goal_temp.theta = math.atan2(self.goal_pose_2d.y, self.goal_pose_2d.x)
                if goal_temp.theta > 0:
                    twist.angular.z = 0.1
                elif goal_temp.theta < 0:
                    twist.angular.z = -0.1
                self.timer.wait(cal_wait_time(goal_temp, twist))
                self.goal_pose_2d.theta -= goal_temp.theta
                self.controlModule.base.set_twist(twist)
                self.change_state('send_theta_goal_before_start_to_slide')
            else:
                if self.goal_pose_2d.x > 0:
                    twist.linear.x = 0.2
                elif self.goal_pose_2d.x < 0:
                    twist.linear.x = -0.2

                elif self.goal_pose_2d.y > 0:
                    twist.linear.y = 0.1
                elif self.goal_pose_2d.y < 0:
                    twist.linear.y = -0.1

                self.timer.wait(cal_wait_time(self.goal_pose_2d, twist))
                self.controlModule.base.set_twist(twist)
                self.change_state('send_xy_goal')

        elif self.state is 'send_theta_goal_before_start_to_slide':
            if not self.timer.is_waiting():
                twist = Twist()
                twist.linear.x = 0.2
                self.timer.wait(cal_wait_time(self.goal_pose_2d, twist))
                self.controlModule.base.set_twist(twist)
                self.change_state('send_xy_goal')

        elif self.state is 'send_xy_goal':
            if not self.timer.is_waiting():
                twist = Twist()
                if self.goal_pose_2d.theta > 0:
                    twist.angular.z = 0.2
                elif self.goal_pose_2d.theta < 0:
                    twist.angular.z = -0.2
                self.timer.wait(cal_wait_time(self.goal_pose_2d, twist))
                self.controlModule.base.set_twist(twist)
                self.change_state('send_theta_goal')

        elif self.state is 'send_theta_goal':
            if not self.timer.is_waiting():
                self.controlModule.base.set_twist_stop()
                print 'finish'
                self.change_state('succeeded')

        self.is_performing = False


def cal_wait_time(goal_pose2d, twist):
    t_linear = 0
    t_angular = 0
    if math.hypot(twist.linear.x, twist.linear.y):
        t_linear = math.hypot(goal_pose2d.x, goal_pose2d.y) / math.hypot(twist.linear.x, twist.linear.y)
        t_linear *= 1.05
    else:
        print 'no linear'

    if twist.angular.z:
        t_angular = goal_pose2d.theta / twist.angular.z
        t_angular *= 0.92
    else:
        print 'no angular'

    print('goal', goal_pose2d)
    print('t_linear', t_linear)
    print ('t_angular', t_angular)

    return t_linear + t_angular
