from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "AThousandYears"


class MoveBaseRelative(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.is_active = False

    def stop(self):
        self.change_state('active')
        self.controlModule.base.set_relative_position(0.0, 0.0, 0.0)

    def set_position(self, dx, dy, dtheta):
        self.change_state('active')
        self.controlModule.base.set_relative_position(dx, dy, dtheta)

    def set_position_without_clear_costmap(self, dx, dy, dtheta):
        self.change_state('active')
        self.controlModule.base.set_relative_position_without_clear_costmap(dx, dy, dtheta)

    def clear_point_costmaps(self, x, y, box_size):
        self.change_state('active')
        self.controlModule.base.clear_point_costmaps(x, y, box_size)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.BASE_STATUS:
                # TODO: Bad code here!!
                self.is_active = MoveBaseStatus.is_active(perception_data.input)
                state = MoveBaseStatus.get_state_from_status(perception_data.input)
                self.change_state(state)

    def clear_costmap(self):
        self.controlModule.base.clear_costmap()
