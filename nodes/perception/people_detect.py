import rospy
import tf
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from people_detection.msg import PersonObjectArray

__author__ = 'AThousandYears'


class PeopleDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        self.tf_listener = tf.TransformListener()
        rospy.Subscriber("/people_detection/people_array", PersonObjectArray, self.callback_people_array)

    def callback_people_array(self, data):
        person_array = self.tf_listener.transformPoint('odom', data)
        print person_array.point
        self.broadcast(Devices.PEOPLE, data.persons)
