__author__ = 'nicole'
import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from geometry_msgs.msg import PointStamped


class GestureDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/gesture/point", PointStamped, self.callback_gesture())

    def callback_gesture(self, data):
        self.broadcast(Devices.GESTURE, data)