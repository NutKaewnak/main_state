from include.abstract_subtask import AbstractSubtask
from include.delay import Delay

__author__ = 'Nicole'


class SearchWavingPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.timer = Delay()
        self.limit_up = 0.9  # pan
        self.limit_down = -0.9
        self.neck_direction = 'right'
        self.waving_people_point = None
        self.new_neck_point = 0.3

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.subtask = self.subtaskBook.get_subtask(self, 'DetectWavingPeople')
            self.timer.wait(3)
            self.change_state('searching')

        elif self.state is 'searching':
            if self.subtask.state is 'finish':
                self.waving_people_point = self.subtask.get_point()
                self.change_state('finish')
            elif not self.timer.is_waiting():
                self.change_state('prepare_to_turn_neck')

        elif self.state is 'prepare_to_turn_neck':
            if perception_data.device is 'NECK':
                pan = perception_data.input.pan
                if self.neck_direction is 'right':
                    if pan + 0.3 <= self.limit_up:
                        self.new_neck_point = 0.3
                    else:
                        self.new_neck_point = self.limit_up - pan
                        self.neck_direction = 'left'
                else:
                    if self.pan - 0.3 >= self.limit_down:
                        self.new_neck_point = -0.3
                    else:
                        self.new_neck_point = self.limit_down + pan
                        self.neck_direction = 'right'

        elif self.state is 'turn_neck':
            self.skill.turn_relative(0, self.new_neck_point)
            if self.skill.state is 'succeeded':
                self.timer.wait(3)
                self.change_state('searching')
