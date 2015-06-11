__author__ = 'Nicole'

import rospy

from include.abstract_subtask import AbstractSubtask


class PickFromPoint(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'init':
            # check if skill is succeed
            self.skill = self.skillBook.get_skill(self, 'pick')
            if self.skill.state is 'succeed':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                self.change_state('error')

    def pick_point(self, goal):
        if self.skillBook is not None:
            self.skill.pick_from_point(goal)