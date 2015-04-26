__author__ = 'nicole'


import rospy

from include.abstract_subtask import AbstractSubtask


class LeaveArena(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('exit')
            self.change_state('MoveToExit')
        elif self.state is 'MoveToExit':
            if self.subtask.state is 'finish':
                self.change_state('finish')
            elif self.subtask.state is 'error':
                self.change_state('error')

            # Don't forget to add this subtask to subtask book
