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
            self.skill.say('Hello, my name is Lam-yai. I am ready to serve you.')
            self.change_state('saying')

        elif self.state is 'saying':
            if self.skill.state is 'succeeded':
                self.change_state('finish')
