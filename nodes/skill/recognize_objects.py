from object_recognition_v2.msg import RecognizeObjectsResult, ObjectRecognition
from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "Frank"


class RecognizeObjects(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.object = None

    def recognize(self, object_names):
        self.change_state('active')
        self.controlModule.recognize_objects.set_new_goal(object_names)

    def perform(self, perception_data):
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.RECOGNIZE_OBJECTS:
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                self.change_state(status)
                if self.state is 'succeeded':
                    self.object = perception_data.input
