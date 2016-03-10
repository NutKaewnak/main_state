import rospy
import tf
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from geometry_msgs.msg import PointStamped

__author__ = 'nicole'


class GestureDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/gesture/points", PointStamped, self.callback_gesture_point)
        self.tf_listener = tf.TransformListener()

    def callback_gesture_point(self, data):
        # data.point.y *= -1
        # data.point.x *= -1
        data.header.stamp = rospy.Time(0)
        point_tf = self.tf_listener.transformPoint('base_link', data)
        print 'point_tf.point ' + str(point_tf.point)
        self.broadcast(Devices.GESTURE, point_tf.point)
