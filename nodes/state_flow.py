#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty

__author__ = 'Frank'


class StateFlow:

    def __init__(self):
        rospy.init_node('state_flow')
        if rospy.has_param('~rate'):
            hz = rospy.get_param('~rate')
        else:
            hz = 1.3
        self.pub = rospy.Publisher('~runner', Empty, queue_size=1)
        self.rate = rospy.Rate(hz)
        self.loop()

    def loop(self):
        while not rospy.is_shutdown():
            self.pub.publish(Empty())
            self.rate.sleep()

if __name__ == "__main__":
    StateFlow()

