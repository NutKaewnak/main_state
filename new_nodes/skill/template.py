__author__ = 'nicole'
from include.abstract_skill import AbstractSkill


class template(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        # self.controlModule

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('succeed')
            # Don't to forget to add this skill to skill book
