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
        rospy.Subscriber("/people_detection_node/peoplearray", PersonObjectArray, self.callback_people_array)

    def callback_people_array(self, data):
        # person_array = []
        # for x in data.persons:
        #     person_array.append(self.tf_listener.transformPoint('odom', x.personpoints))
        # print person_array
        # print data
        self.broadcast(Devices.PEOPLE, data.persons)
