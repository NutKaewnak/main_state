from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = 'nicole'


class SetHeightRelative(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def stop(self):
        self.change_state('active')
        self.controlModule.torso.set_height_relative(0.0)

    def set_position(self, dx):
        self.change_state('active')
        self.controlModule.torso.set_height_relative(dx)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.HEIGHT:
                state = MoveBaseStatus.get_state_from_status(perception_data.input)
                self.change_state(state)
                # Don't to forget to add this skill to skill book
