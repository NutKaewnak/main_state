__author__ = 'nicole'
import rospy
from include.abstract_subtask import AbstractSubtask


class SetHeightRelative(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'start':
            if self.skill.state is 'succeeded':
                self.change_state('finish')

    def set_height(self, data):
        self.skill = self.skillBook.get_skill(self, 'SetHeightRelative')
        self.skill.set_position(data)
        self.change_state('start')
