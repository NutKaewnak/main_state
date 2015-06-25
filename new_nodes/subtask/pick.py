__author__ = 'Nicole'

import rospy
from include.abstract_subtask import AbstractSubtask


class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.input_object_pos = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'Pick')
            self.change_state('wait_object')

        elif self.state is 'receive_object':
            self.skill.pick_object(self.input_object_pos)
            if self.skill.state is 'succeed':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                self.change_state('error')

    def pick_object(self, goal):
        self.input_object_pos = goal
        self.change_state('receive_object')