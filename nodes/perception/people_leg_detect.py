import rospy
import tf
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from people_detection.msg import PersonObjectArray


__author__ = 'Frank Tower'


class PeopleLegDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        self.tf_listener = tf.TransformListener()
        rospy.Subscriber("/people/people_detection/peoplearray", PersonObjectArray, self.callback_people_array)
        # rospy.Subscriber("/people_detection_node/peoplearray", PersonObjectArray, self.callback_people_array)

    def callback_people_array(self, data):
        self.broadcast(Devices.PEOPLE, data=data)
