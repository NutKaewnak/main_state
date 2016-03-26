from clothing_type_classification.msg import FindClothesResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices
import rospy

__author__ = "kandithws"


class ClothesDetectorPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/clothes_detection_node/result', FindClothesResult, self.callback_clothes_detector_status)
        # rospy.Subscriber('/object/recognize_objects/feedback', RecognizeObjectsFeedback, self.callback_base_position)

    def callback_clothes_detector_status(self, data):
        self.broadcast(Devices.CLOTHES_DETECTOR, data)
