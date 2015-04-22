__author__ = "AThousandYears"

import rospy

from include.abstract_subtask import AbstractSubtask


class MoveToLocation(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.move = None

    def to_location(self, location_name):
        location_point = self.get_location_point(location_name)
        self.move = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
        self.move.set_point(location_point)
        self.change_state('move')

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if self.move.state is 'succeed':
                self.change_state('finish')
            elif self.move.state is 'aborted':
                rospy.loginfo('Aborted at MovePassDoor')
                self.change_state('error')