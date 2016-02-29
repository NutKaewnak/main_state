
import rospy
from include.abstract_subtask import AbstractSubtask
__author__ = 'CinDy'

class Gripper(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.griper = self.skillBook.get_skill(self, 'Say')

    def gripper(self, message):

        self.change_state('init')

    def perform(self, perception_data):
        if self.state is 'init':
            if self.speak.state is 'succeeded':
                self.change_state('finish')
