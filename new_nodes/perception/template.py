__author__ = 'nicole'

import rospy
# from std_msgs.msg import String
# from geometry_msgs.msg import PointStamped
from include.abstract_perception import AbstractPerception
from include.devices import Devices


class template(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        # rospy.Subscriber('/base/status', String, self.callback_base_status)
        # rospy.Subscriber("/gesture/point", PointStamped, self.callback_gesture())

    # def callback_base_status(self, data):
    #   self.broadcast(Devices.BASE_STATUS, data)

    # Don't forget to add this perception into perception_module