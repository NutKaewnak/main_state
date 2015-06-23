from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'

class Introduce(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None

    def perform(self, perception_data):
        if self.state is 'init':
            if self.skill is None:
                self.skill = self.skillBook.get_skill(self, 'Say')
                self.skill.say('Hello, my name is Lamyai. I am cooking assistance.')
            self.change_state('finish')
