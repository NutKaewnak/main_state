__author__ = "AThousandYears"

import rospy

from include.abstract_task import AbstractTask


class RIPS(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.move = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state_with_subtask('movePassDoor', 'MovePassDoor')

        elif self.state is 'movePassDoor':
            subtask = self.change_state_with_subtask('moveToTable', 'MoveToLocation')
            if subtask is not None:
                subtask.move.to_location('hallway table')

        elif self.state is 'moveToTable':
            if self.current_subtask.state is 'finish':
                self.subtaskBook.get_subtask('Register')
                self.change_state('moveArm')

        elif self.state is 'moveArm':
            subtask = self.change_state_with_subtask('moveToTable', 'MoveToLocation')
            if subtask is not None:
                subtask.move.to_location('outside_pos')
                self.change_state('success')