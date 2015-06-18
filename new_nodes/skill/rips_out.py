__author__ = 'nicole'
from include.abstract_skill import AbstractSkill


class RipsOut(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def perform(self, perception_data):
        if self.state is 'init':
            controller = self.controlModule.left_arm
            controller.set_action('rips_out')
            self.change_state('succeed')