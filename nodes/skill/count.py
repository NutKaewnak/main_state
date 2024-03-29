from include.abstract_skill import AbstractSkill
from include.delay import Delay

__author__ = 'krit'


class Count(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.time = 0
        self.timer = Delay()

    def count_down(self, time):
        self.state = 'start'
        self.time = time

    def perform(self, perception_data):
        if self.state is 'start':
            self.controlModule.speaker.speak(str(self.time))
            self.time -= 1
            self.timer.wait(1)
            self.change_state('waiting')
        elif self.state is 'waiting':
            if not self.timer.is_waiting() and self.controlModule.speaker.is_finish():
                if self.time <= 0:
                    self.change_state('succeeded')
                else:
                    self.change_state('start')
