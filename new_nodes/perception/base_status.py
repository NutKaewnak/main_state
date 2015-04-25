__author__ = "AThousandYears"

import rospy
from std_msgs.msg import String

from include.abstract_perception import AbstractPerception
from include.devices import Devices


class BaseStatusPerception(AbstractPerception):
    def __init__(self, main_state):
        AbstractPerception.__init__(self, main_state.planningModule)
        rospy.Subscriber('/base/status', String, self.callback_base_status)

    def callback_base_status(self, data):
        self.broadcast(Devices.BASE_STATUS, data)
