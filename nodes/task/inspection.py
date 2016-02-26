__author__ = 'Nutk'
import rospy
import math
from include.abstract_task import AbstractTask
from include.delay import Delay


class Inspection(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('Inspect init')
            self.change_state_with_subtask('move_pass_door', 'MovePassDoor')

        elif self.state is 'move_pass_door':
            if self.current_subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say').say('Hello, my name is Lamyai. I will do inspection')
                rospy.loginfo('going to waypoint 1')
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to living room.')
                self.change_state('prepare_to_living_room')

        elif self.state is 'prepare_to_living_room':
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('living_room')  # must change
            self.change_state('going_to_living_room')

        elif self.state is 'going_to_living_room':
            if self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('I reach living room.')
                self.change_state('prepare_leave_arena')

        elif self.state is 'prepare_leave_arena':
            self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
            self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')