from include.base_state import *

__author__ = 'nicole'
import rospy
import roslib
from std_msgs.msg import *
from lumyai_navigation_msgs.msg import *
from geometry_msgs.msg import *
from function import *


class moveToLocation:
    location = None
    def __init__(self):
        BaseState.__init__(self)

    def toLocation(self, location):
        self.location = location

    def main(self, device, data):
        if self.location is None:
            return

        if self.state == STATE.INIT:
            Publish.move_robot(self.location)

        if device == Devices.base and data == 'SUCCEEDED':
            self.speak('succeeded')
            self.state = STATE.SUCCEEED
        elif device == Devices.base and data == 'ABORTED':
            self.speak('aborted')
            self.state = STATE.ABORTED



if __name__ == '__main__':
    moveToLocation()