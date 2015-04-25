__author__ = "AThousandYears"

import rospy
from std_msgs.msg import String

from include.abstract_perception import AbstractPerception
from include.devices import Devices


class VoicePerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/voice/output', String, self.callback_voice)

    def callback_voice(self, data):
        self.broadcast(Devices.VOICE, data)