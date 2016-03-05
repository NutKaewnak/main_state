from object_3d_detector.msg import Object3DsResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices
import rospy

__author__ = "Frank"


class Object3DsDetectorPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/object/cluster_extraction/result', Object3DsResult, self.callback_objects_detector_status)
        # rospy.Subscriber('/object/recognize_objects/feedback', RecognizeObjectsFeedback, self.callback_base_position)

    def callback_objects_detector_status(self, data):
        self.broadcast(Devices.OBJECT_3DS_DETECTOR, data)
