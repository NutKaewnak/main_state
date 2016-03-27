from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus
from clothing_type_classification.msg import FindClothesResult, ClothesArray

__author__ = "kandithws"


class DetectClothes(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.detected_clothes = FindClothesResult()

    def detect(self):
        self.change_state('active')
        self.detected_clothes = None
        self.controlModule.clothes_detector.set_new_goal()

    def perform(self, perception_data):
        if self.state is 'active':
            if perception_data.device is self.Devices.CLOTHES_DETECTOR:
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                self.change_state(status)

            if self.state is 'succeeded':
                if not perception_data.input.result.array:
                    self.change_state('not_found')
                self.detected_clothes = perception_data.input.result.array
