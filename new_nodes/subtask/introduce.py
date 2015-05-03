from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'

class Introduce(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('Hello, my name is Lamyai. I am from Kasetsart university.')
            self.change_state('rips_out')

        elif self.state is 'rips_out':
            self.skill = self.skillBook.get_skill(self, 'RipsOut')
            self.change_state('finish')
