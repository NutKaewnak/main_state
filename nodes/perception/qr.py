from std_msgs.msgs import String
from include.abstract_perception import AbstractPerception
from include.devices import Devices
import rospy

__author__ = "Frank"


class RecognizeObjectsPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/barcode', String, self.callback_qr)
    def callback_qr(self, data):
        self.broadcast(Devices.VOICE, data.da)
