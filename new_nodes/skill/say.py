__author__ = 'nicole'
from include.abstract_skill import AbstractSkill


class Say(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def say(self, message):
        if self.state is 'init':
            self.controlModule.speaker.speak(message)
            self.change_state('succeed')