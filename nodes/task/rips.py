__author__ = "AThousandYears"

import rospy

from include.abstract_task import AbstractTask


class RIPS(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.move = None
        self.subtask = None
    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('movePassDoor')

        elif self.state is 'movePassDoor':
            if self.subtask.state is 'finished':
                subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                subtask.to_location('check_point')
                self.change_state('moveToCheckpoint')

        elif self.state is 'moveToCheckpoint':
            if self.current_subtask.state is 'finish':
                if perception_data.device is 'VOICE' and perception_data.input:
                    if perception_data.input == 'countinue':
                        pass

                self.subtaskBook.get_subtask('Register')
                self.change_state('moveArm')

        elif self.state is 'moveArm':
            subtask = self.change_state_with_subtask('moveToTable', 'MoveToLocation')
            if subtask is not None:
                subtask.to_location('outside_pos')
                self.change_state('finish')