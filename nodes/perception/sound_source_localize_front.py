import rospy
from hark_msgs.msg import HarkSource
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = "Nathas"


class SoundSourceLocalizeFront(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/HarkSourceFront', HarkSource, self.callback_voice)

    def callback_voice(self, data):
        self.broadcast(Devices.HARK_SOURCE_FRONT, data)
