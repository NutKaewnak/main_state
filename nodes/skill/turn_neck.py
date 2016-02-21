__author__ = 'Nicole'
from include.abstract_skill import AbstractSkill
from include.neck_status import NeckStatus


class TurnNeck(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck
        self.pan = 0
        self.tilt = 0
        self.pitch = 0
        self.yaw = 0

    def perform(self, perception_data):
        if self.state is 'active' or self.state is 'pending':
            if perception_data.device is 'NECK':
                self.pan = perception_data.input.pan
                self.tilt = perception_data.input.tilt
                state = NeckStatus.get_state_from_status(perception_data.input.status)
                self.change_state(state)

        if self.state is 'receive':
            if perception_data.device is 'NECK':
                self.pan = perception_data.input.pan
                self.tilt = perception_data.input.tiltfoll
                self.turn(self.pitch + self.tilt, self.yaw + self.pan)

    def turn(self, pitch, yaw):
        self.neck.set_neck_angle(pitch, yaw)
        self.change_state('active')

    def turn_relative(self, pitch, yaw):
        self.pitch = pitch
        self.yaw = yaw
        print 'turn_relative---------'
        self.change_state('receive')

