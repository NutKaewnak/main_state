# Not yet finish
__author__ = 'Nicole'

import actionlib
from include.abstract_skill import AbstractSkill
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryFeedback
from control_msgs.msg import FollowJointTrajectoryResult


class TurnNeck(AbstrackSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck
        client = actionlib.SimpleActionClient('do_dishes', FollowJointTrajectoryAction)
        # self.controlModule

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('succeed')
            # Don't to forget to add this skill to skill book

    def turn(self, angle):
        self.neck.set_neck_angle(0, angle)