from include.abstract_skill import AbstractSkill

__author__ = 'nicole'


class Template(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        # self.controlModule

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('succeeded')
            # Don't to forget to add this skill to skill book
