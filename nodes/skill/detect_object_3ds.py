from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "Frank"

class DetectObject3Ds(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.objects = None

    def detect(self):
        self.change_state('active')
        self.controlModule.detect_object_3ds.set_new_goal()

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.RECOGNIZE_OBJECTS:
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                self.change_state(status)
                if self.state is 'succeeded':
                    self.objects = perception_data.input.result
