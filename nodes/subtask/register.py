__author__ = 'nicole'

import rospy
from include.abstract_subtask import AbstractSubtask


class Register(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'RipsOut')
            self.change_state('succeed')