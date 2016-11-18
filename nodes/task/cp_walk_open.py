from include.abstract_task import AbstractTask
from include.delay import Delay
from math import pi
import rospkg
import os
__author__ = 'cindy'


class CPWalkOpen(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init' and perception_data.device is self.Devices.STATE_FLOW:
            self.delay = Delay()
            rospack = rospkg.RosPack()
            self.path = rospack.get_path('main_state')
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
            self.subtask.set_position(2, 0, 0)
            self.change_state('check_move')

        elif self.state is 'check_move':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask.play(os.path.join(self.path, 'robot_sound', 'sound', 'greeting_eng.wav'))
                self.delay.wait(10)
                self.change_state('move_back')

        elif self.state is 'move_back' and perception_data.device is self.Devices.STATE_FLOW:
            if not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_position(-2, 0, 0)
                self.change_state('check_move_back')

        elif self.state is 'check_move_back':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_position(1, 0, 0)
                self.change_state('finish')
