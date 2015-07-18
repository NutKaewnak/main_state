__author__ = 'Nicole'
from include.abstract_skill import AbstractSkill
from include.neck_status import NeckStatus


class TurnNeck(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck
        self.pan = None
        self.tilt = None

    def perform(self, perception_data):
        if self.state is 'active':
            if perception_data.device is 'NECK':
                self.pan = perception_data.input.pan
                self.tilt = perception_data.input.tilt
                state = NeckStatus.get_state_from_status(perception_data.input.status)
                self.change_state(state)

    def turn(self, pitch, yaw):
        self.neck.set_neck_angle(pitch, yaw)
        self.change_state('active')

    def turn_relative(self, pitch, yaw):
        self.turn(pitch + self.tilt, yaw + self.pan)
