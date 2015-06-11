# Not yet finish
__author__ = 'Nicole'


class TurnNeck(AbstrackSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('succeed')
            # Don't to forget to add this skill to skill book

    def turn(self, pitch, yaw):
        self.neck.set_neck_angle(pitch, yaw)

    def turn_relative(self, pitch, yaw):
        self.neck.set_neck_angle_relative(pitch, yaw)