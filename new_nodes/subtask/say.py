__author__ = 'nicole'
import rospy

from include.abstract_subtask import AbstractSubtask


class Say(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.speak = self.skillBook.get_skill(self, 'Say')

    def say(self, message):
        self.speak.say(message)
        self.change_state('saying')

    def perform(self, perception_data):
        if self.state is 'saying':
            self.change_state('succeed')

# Don't forget to add this subtask to subtask book