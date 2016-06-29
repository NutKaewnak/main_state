from std_msgs.msg import String
from include.abstract_perception import AbstractPerception
from include.devices import Devices
import rospy

__author__ = "Frank"


class Qr(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/z_bar/barcode', String, self.callback_qr)

    def callback_qr(self, data):
        print data
        self.broadcast(Devices.VOICE, data.data)
