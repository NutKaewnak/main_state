__author__ = 'Nicole'
from include.abstract_skill import AbstractSkill


class Pick(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('waiting')

    def pick_from_point(self, goal):
        self.change_state('init')
        self.controlModule.manipulator.manipulate('right_arm', goal)
        self.change_state('succeed')