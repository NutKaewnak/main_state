from include.base_state import BaseState, STATE

__author__ = 'nicole'
import rospy
import roslib
from std_msgs.msg import *
from lumyai_navigation_msgs.msg import *
from geometry_msgs.msg import *
from include.publish import Publish
from include.base_state import Devices

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
        self.state = STATE.INIT

    def main(self, device, data):
        if self.state is STATE.INIT:
            if self.x is not None and self.y is not None and self.z is not None:
                Publish.move_relative(self.x, self.y, self.z)
                self.x = None
                self.y = None
                self.z = None
        elif device is Devices.base and data is 'SUCCEEDED':
            self.speak('succeeded')
            self.state = STATE.SUCCEEED
        elif device is Devices.base and data is 'ABORTED':
            self.speak('aborted')
            self.state = STATE.ABORTED