import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from geometry_msgs.msg import PointStamped
from std_msgs.msg import String


__author__ = 'Frank Tower'


class DoorHandleDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/door_handle_detection/PointStamped", PointStamped, self.callback_handle)

    def callback_handle(self, data):
        self.broadcast(Devices.DOOR_HANDLE, data)
