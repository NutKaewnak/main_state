__author__ = 'nicole'
import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from geometry_msgs.msg import Vector3


class GestureDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/gesture/point", Vector3, self.callback_gesture_point)

    def callback_gesture_point(self, data):
        self.broadcast(Devices.GESTURE, data)