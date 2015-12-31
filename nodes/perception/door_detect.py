import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from std_msgs.msg import String

__author__ = 'nicole'


class DoorDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/door/status", String, self.callback_door_status)

    def callback_door_status(self, data):
        self.broadcast(Devices.DOOR, data.data)
