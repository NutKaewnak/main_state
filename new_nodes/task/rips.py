__author__ = "AThousandYears"

import rospy

from include.abstract_task import AbstractTask


class RIPS(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.move = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.move = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('movePassDoor')
        elif self.state is 'movePassDoor':
            if self.move.state is 'finish':
                self.move = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.move.to_location('hallway table')
                self.change_state('moveToTable')
        elif self.state is 'moveToTable':
            if self.move.state is 'finish':
                self.change_state('finish')