import rospy
from std_msgs.msg import String
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = "Frank Tower"


class GuessObjectPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/guess_detection/guess_object', String, self.callback_voice)

    def callback_voice(self, data):
        self.broadcast(Devices.GUESS_OBJECT, data.data)
