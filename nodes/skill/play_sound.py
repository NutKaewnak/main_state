from include.abstract_skill import AbstractSkill

__author__ = 'cindy'


class PlaySound(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def play(self, sound):
        self.controlModule.sound_player.speak(sound)
        self.change_state('saying')

    def terminate_sound(self):
        self.controlModule.sound_player.terminate_sound()
        self.change_state('aborted')

    def perform(self, perception_data):
        if self.state is 'saying':
            if self.controlModule.sound_player.is_finish():
                self.change_state('succeeded')
