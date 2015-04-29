__author__ = 'AThousandYears'

import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from people_detection.msg import  PersonObjectArray


class PeopleDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/people_detection/people_array", PersonObjectArray, self.callback_people_array)

    def callback_people_array(self, data):
        self.broadcast(Devices.PEOPLE, data.persons)
