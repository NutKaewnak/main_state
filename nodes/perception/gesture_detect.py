import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from geometry_msgs.msg import PointStamped

__author__ = 'nicole'


class GestureDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/gesture/points", PointStamped, self.callback_gesture_point)

    # FIXME the either axis transformation or the gesture node is incorrect
    def callback_gesture_point(self, data):
        data.point.y *= -1
        data.point.x *= -1
        self.broadcast(Devices.GESTURE, data.point)
