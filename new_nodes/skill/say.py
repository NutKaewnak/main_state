__author__ = 'nicole'
import rospy
from include.abstract_skill import AbstractSkill


class Say(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def say(self, message):
        self.controlModule.speaker.speak(message)
        rospy.loginfo('saying: ' + message)
        self.change_state('saying')

    def perform(self, perception_data):
        if self.state is 'saying':
            self.change_state('succeeded')