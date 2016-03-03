import rospy
import actionlib
from speech_processing.msg import VoiceRegGoal, VoiceRegAction
from std_msgs.msg import String

__author__ = "Frank"


class VoiceRecognitionModeContoller:
    def __init__(self):
        self.voice_recognition_mode = actionlib.SimpleActionClient('/recognizer/voice_reg', VoiceRegAction)

    def set_new_goal(self):
        self.voice_recognition_mode.send_goal(VoiceRegGoal())
