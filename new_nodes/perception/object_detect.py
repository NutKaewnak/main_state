__author__ = 'Nicole'

import rospy
# from std_msgs.msg import String
from geometry_msgs.msg import Point
from object_detection.msg import ObjectDetection
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class ObjectDetect(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/object_shape', ObjectDetection, self.callback_object_point)

    def callback_object_point(self, data):
        self.broadcast(Devices.OBJECT, data)