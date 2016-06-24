__author__ = "AThousandYears"

import rospy

from include.abstract_subtask import AbstractSubtask


class MoveRelative(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.moveRelative = None

    def set_position(self, x, y, theta):
        self.moveRelative = self.skillBook.get_skill(self, 'MoveBaseRelative')
        self.moveRelative.set_position(x, y, theta)
        self.change_state('move')

    def set_position_without_clear_costmap(self, x, y, theta):
        self.moveRelative = self.skillBook.get_skill(self, 'MoveBaseRelative')
        self.moveRelative.set_position(x, y, theta)
        self.change_state('move')

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if self.moveRelative.state is 'succeeded':
                self.change_state('finish')
            elif self.moveRelative.state is 'aborted':
                rospy.loginfo('Aborted')
                self.change_state('error')
