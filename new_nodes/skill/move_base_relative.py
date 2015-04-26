__author__ = "AThousandYears"

from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus


class MoveBaseRelative(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def set_position(self, dx, dy, dtheta):
        self.change_state('active')
        self.controlModule.base.set_relative_position(dx, dy, dtheta)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.BASE_STATUS:
                state = MoveBaseStatus.get_state_from_status(perception_data)
                self.change_state(state)