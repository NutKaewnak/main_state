from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "AThousandYears"


class MoveBaseAbsolute(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.is_active = False

    def set_point(self, point):
        self.set_position(point.x, point.y, point.z)

    def set_position(self, x, y, theta):
        self.change_state('active')
        self.controlModule.base.clear_costmaps()
        # print('--clear costmap--')
        self.controlModule.base.set_absolute_position(x, y, theta)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.BASE_STATUS:
                state = MoveBaseStatus.get_state_from_status(perception_data.input)
                # TODO: Bad code here!!
                print '*****move****'
                print 'perception = '+str(perception_data.input)
                self.is_active = MoveBaseStatus.is_active(perception_data.input)
                print "movebase_isactive" + str(self.is_active)
                self.change_state(state)
