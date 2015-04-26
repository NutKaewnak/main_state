__author__ = 'nicole'

from include.abstract_skill import AbstractSkill
from include.delay import Delay
import math


class TurnNeckForSearchPeople(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck
        self.timer = Delay()
        self.angle = None

    def perform(self, perception_data):
        if self.state is 'waitingForNeck':
            if perception_data.device is self.Devices.NECK and perception_data.input is 'SUCCEED':
                self.change_state('waitAtStart')

        elif self.state is 'start':
            self.angle += 0.3
            self.neck.turn(0, self.angle)
            self.timer.wait(3)
            if self.angle >= 90*math.pi/180:
                self.change_state('succeed')
        elif self.state is 'stop':
            if perception_data.device is self.Devices.NECK and perception_data.input is 'SUCCEED':
                self.change_state('stopped')

    def prepare(self):
        self.angle = -90*math.pi/180
        self.neck.turn(0, self.angle)
        self.change_state('waitingForNeck')

    def start(self):
        if self.state is not 'waitAtStart':
            return
        self.change_state('start')

    def stop(self):
        self.change_state('stop')