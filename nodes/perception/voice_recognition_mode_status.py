from speech_processing.msg import VoiceRegFeedback, VoiceRegResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices
import rospy

__author__ = "Frank"


class VoiceRecognitionModePerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/recognizer/voice_reg/result', VoiceRegResult, self.callback_voice_recognition_mode_status)
        # rospy.Subscriber('/object/recognize_objects/feedback', RecognizeObjectsFeedback, self.callback_base_position)

    def callback_voice_recognition_mode_status(self, data):
        self.broadcast(Devices.VOICE_MODE, data)
