__author__ = "AThousandYears"

import rospy

from include.abstract_subtask import AbstractSubtask


class MovePassDoor(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.moveRelative = None

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is self.Devices.DOOR and perception_data.input == 'open':
                self.moveRelative = self.skillBook.get_skill(self, 'MoveBaseRelative')
                self.moveRelative.set_position(2.5, 0.0, 0.0)
                self.change_state('move')
        elif self.state is 'move':
            # check if base succeed
            if self.moveRelative.state is 'succeeded':
                self.change_state('finish')
            elif self.moveRelative.state is 'aborted':
                rospy.loginfo('Aborted at MovePassDoor')
                self.change_state('error')
