__author__ = "AThousandYears"

from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus


class MoveBaseAbsolute(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def set_point(self, point):
        self.set_position(point.x, point.y, point.z)

    def set_position(self, x, y, theta):
        self.change_state('active')
        self.controlModule.base.set_absolute_position(x, y, theta)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.BASE_STATUS:
                state = MoveBaseStatus.get_state_from_status(perception_data.input)
                print state
                self.change_state(state)