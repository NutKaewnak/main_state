__author__ = "AThousandYears"

from include.abstract_skill import AbstractSkill


class MoveBaseRelative(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def set_position(self, dx, dy, dtheta):
        self.change_state('move')
        (x, y, theta) = self.get_current_position()
        self.controlModule.base.set_position(x+dx, y+dy, theta+dtheta)

    def get_current_position(self):
        if self.perception_module.base_position.current_input is None:
            return 0.0, 0.0, 0.0
        else:
            return self.perception_module.base_position.current_input

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if perception_data.device is self.Devices.BASE_STATUS and perception_data.input is 'SUCCEED':
                self.change_state('succeed')