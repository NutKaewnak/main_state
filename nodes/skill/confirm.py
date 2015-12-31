from include.abstract_skill import AbstractSkill

__author__ = 'nicole'


class Confirm(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        # self.controlModule

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.input is 'robot yes':
                self.change_state('confirm')
            elif perception_data.input is 'robot no':
                self.change_state('negative')
