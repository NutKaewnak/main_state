__author__ = 'nicole'
import rospy

from include.abstract_subtask import AbstractSubtask


class Say(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.speak = self.skillBook.get_skill(self, 'Say')
        self.message = None

    def perform(self, perception_data):
        if self.state is 'saying':
            if self.speak.state is 'succeeded':
                self.change_state('finish')

    def say(self, message):
        self.message = message
        self.speak.say(self.message)
        self.change_state('saying')
