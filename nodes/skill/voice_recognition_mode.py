from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "Frank"

class VoiceRecognitionMode(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)

    def recognize(self, id):
        self.change_state('active')
        self.controlModule.voice_recognition_mode.set_new_goal(id)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.VOICE_MODE:
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                self.change_state(status)
