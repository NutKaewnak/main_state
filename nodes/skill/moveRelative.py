from include.base_state import BaseState, STATE

__author__ = 'nicole'
import rospy
import roslib
from std_msgs.msg import *
from lumyai_navigation_msgs.msg import *
from geometry_msgs.msg import *
from include import publish

roslib.load_manifest('main_state')

class moveRelative:
    def __init__(self):
        BaseState.__init__(self)
        self.x = None
        self.y = None
        self.z = None
        rospy.loginfo('Move relative to '+self.x+' : '+self.y+' : '+self.z)
        rospy.spin()

    def to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def main(self, device, data):
        if self.state == STATE.INIT:
            if self.x is not None and self.y is not None and self.z is not None:
                publish.move_relative(self.x, self.y, self.z)
