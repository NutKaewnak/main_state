import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'cindy'


class PlaySound(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'PlaySound')

    def perform(self, perception_data):
        if self.state is 'playing':
            if self.skill.state is 'succeeded':
                self.change_state('finish')

    def play(self, sound):
        print sound
        self.skill.play(sound)
        self.change_state('playing')

    def terminate_sound(self):
        self.skill.terminate_sound()
        print '------------------skill ', self.skill.state
        self.change_state('aborted')
