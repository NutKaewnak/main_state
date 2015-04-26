__author__ = 'nicole'
from include.abstract_skill import AbstractSkill

class DetectPeopleWithGesture(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        # self.controlModule
        self.pos = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('searching')

        elif self.state is 'searching':
            if perception_data.device is self.Devices.gesture:
                self.pos = perception_data.input
                self.change_state('succeeded')

    def start(self):
        self.pos = None
        self.change_state('init')

    def getPos(self):
        return self.pos