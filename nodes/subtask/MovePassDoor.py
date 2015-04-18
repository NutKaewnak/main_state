from factory.move import Move
from factory.neck import Neck

__author__ = 'nicole'
import rospy
import roslib
from include.base_state import *
from math import pi

class MovePassDoor(BaseState):
    def __init__(self):
        BaseState.__init__(self)

        Publish.set_height(1.0)
        rospy.loginfo('Start move pass door State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if self.state == STATE.INIT:
            if device == Devices.door and data == 'open':
                Move.relative.to(1.5, 0)
                self.state = STATE.PASSDOOR
            Neck.lookDown()
            Publish.set_manipulator_action('walking')
        elif device == Devices.base and data == 'SUCCEEDED':
            self.state = STATE.SUCCEEED
        elif device == Devices.base and data == 'ABORTED':
                self.speak('aborted')
                self.state = STATE.ERROR


if __name__ == '__main__':
    MovePassDoor()
