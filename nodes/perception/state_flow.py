import rospy
from std_msgs.msg import Empty
# from geometry_msgs.msg import PointStamped
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'Frank'


class StateFlow(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/state_flow/runner', Empty, self.callback)

    def callback(self, data):
      self.broadcast(Devices.STATE_FLOW, data)

