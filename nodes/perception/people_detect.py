import rospy
import tf
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from people_detection.msg import PersonObjectArray
from geometry_msgs.msg import PointStamped

__author__ = 'AThousandYears'


class PeopleDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        self.tf_listener = tf.TransformListener()
        rospy.Subscriber("/people/people_detection/peoplearray", PersonObjectArray, self.callback_people_array)
        # rospy.Subscriber("/people_detection_node/peoplearray", PersonObjectArray, self.callback_people_array)

    def callback_people_array(self, data):
        person_array = []
        for x in data.persons:
            temp = PointStamped()
            temp.header = data.header
            temp.point = x.personpoints
            x.personpoints = temp
            person_array.append(x)
        self.broadcast(Devices.PEOPLE, person_array)
