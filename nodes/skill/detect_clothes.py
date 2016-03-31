from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus
from clothing_type_classification.msg import FindClothesResult, Clothes

__author__ = "kandithws"


class DetectClothes(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.detected_clothes = FindClothesResult()

    def detect(self):
        self.change_state('active')
        self.detected_clothes = None
        self.controlModule.cloth_detector.set_new_goal()

    def perform(self, perception_data):
        if self.state is 'active':
            if perception_data.device is self.Devices.CLOTHES_DETECTOR:
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                self.change_state(status)

            if self.state is 'succeeded':
                if not perception_data.input.result.result.array:
                    self.change_state('not_found')
                self.detected_clothes = perception_data.input.result.result.array
                temp = self.detected_clothes[0].centroid.y
                j = 0
                for i in range(len(self.detected_clothes)):
                    if temp < self.detected_clothes[i].centroid.y:
                        temp = self.detected_clothes[i].centroid.y
                        j = i
                self.detected_clothes.pop(j)
                print 'detected clothes ', self.detected_clothes

