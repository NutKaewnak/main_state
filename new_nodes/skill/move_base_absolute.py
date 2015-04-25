__author__ = "AThousandYears"

from include.abstract_skill import AbstractSkill


class MoveBaseAbsolute(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def set_position(self, x, y, theta):
        self.change_state('move')
        self.controlModule.base.set_position(x, y, theta)

    def set_point(self, point):
        self.change_state('move')
        self.controlModule.base.set_position(point.x, point.y, point.theta)

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if perception_data.device is self.Devices.BASE_STATUS and perception_data.input is 'SUCCEED':
                self.change_state('succeed')