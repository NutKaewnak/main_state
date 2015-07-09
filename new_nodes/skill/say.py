import math

__author__ = 'nicole'

import re
import rospy
from include.delay import Delay
from include.abstract_skill import AbstractSkill


class Say(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.delay = Delay()

    def say(self, message):
        self.controlModule.speaker.speak(message)
        rospy.loginfo('saying: ' + message)
        wait_time = len(re.findall(r'\w+', message))
        self.delay.wait(math.ceil(wait_time / 2.0) + 1)
        self.change_state('saying')

    def perform(self, perception_data):
        if self.state is 'saying':
            if not self.delay.is_waiting():
                self.change_state('succeeded')