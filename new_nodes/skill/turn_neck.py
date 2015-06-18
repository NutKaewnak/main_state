# Not yet finish
__author__ = 'Nicole'
from include.abstract_skill import AbstractSkill


class TurnNeck(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck
        self.pan = None
        self.tilt = None

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is 'NECK':
                self.pan = perception_data.input.pan
                self.tilt = perception_data.input.tilt
                self.change_state('succeed')
            # Don't to forget to add this skill to skill book

    def turn(self, pitch, yaw):
        self.neck.set_neck_angle(pitch, yaw)

    def turn_relative(self, pitch, yaw):
        self.change_state('init')
        self.neck.set_neck_angle(pitch + self.tilt, yaw + self.pan)
