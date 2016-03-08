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
        rospy.Subscriber("/people_detection_node/peoplearray", PersonObjectArray, self.callback_people_array)

    def callback_people_array(self, data):
        person_array = []
        print data
        print 'kuy'
        for x in data.persons:
            print 'x ='+ str(x)
            temp = PointStamped()
            temp.header = data.header
            temp.point = x.personpoints
            print 'temp = '+str(temp)
            print 'temp.point = '+str(temp.point)
            person_array.append(self.tf_listener.transformPoint('odom', temp))
        print person_array
        self.broadcast(Devices.PEOPLE, data.persons)
