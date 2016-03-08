__author__ = "AThousandYears"

import rospy

from include.abstract_subtask import AbstractSubtask


class MoveAbsolute(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.moveAbsolute = None

    def set_position(self, x, y, theta):
        print '--moveAbsolute.set_position--'
        self.moveAbsolute = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
        self.moveAbsolute.set_position(x, y, theta)
        self.change_state('move')

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if self.moveAbsolute.state is 'succeeded':
                self.change_state('finish')
            elif self.moveAbsolute.state is 'aborted':
                rospy.loginfo('Aborted')
                self.change_state('error')
