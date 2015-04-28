import rospy

__author__ = 'nicole'
from include.abstract_skill import AbstractSkill

class DetectPeopleWithGesture(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        # self.controlModule
        self.pos = None

    def perform(self, perception_data):
        rospy.loginfo('DetectPeopleWithGesture'+self.state)
        if self.state is 'init':
            self.pos = None
            self.change_state('searching')

        elif self.state is 'searching':
            if perception_data.device is self.Devices.GESTURE:
                rospy.loginfo(type(perception_data.input))
                self.pos = perception_data.input
                self.change_state('succeeded')

    def start(self):
        self.pos = None
        self.change_state('init')

    def get_point(self):
        return self.pos