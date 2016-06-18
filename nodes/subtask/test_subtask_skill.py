import rospy
import math
from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class TestSubtaskSkill(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'MoveBaseRelativeTwist')
            print 'send goal'
            self.skill.set_position(0.20, -0.20, 0)
            self.change_state('wait_for_skill')

        elif self.state is 'wait_for_skill':
            if self.skill.state is 'succeeded':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                rospy.loginfo('Aborted')
                self.change_state('error')
