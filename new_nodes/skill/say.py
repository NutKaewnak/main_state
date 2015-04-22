__author__ = 'nicole'
from include.abstract_skill import AbstractSkill


class Say(AbstractSkill):
    def __init__(self):
        AbstractSkill.__init__(self)

    def say(self, message):
        self.controlModule.speaker.speak(message)