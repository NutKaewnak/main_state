#!/usr/bin/env python
import rospy
import roslib
from factory.move import Move
from include.function import *
from include.publish import *
from include.base_state import *
from math import pi


class  RIPS(BaseState):
    def __init__(self):
        BaseState.__init__(self)

        Publish.set_height(1.0)
        rospy.loginfo('Start RIPS State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if self.state == STATE.INIT:
            Move.passDoor()
            self.state = STATE.PASSDOOR

        elif self.state == STATE.PASSDOOR and Move.passDoor().state == STATE.SUCCEED:
            Move.toLocation('hallway table')
            self.state = 'goToTable'

        elif self.state == 'goToTable':
            if Move.toLocation().state == STATE.SUCCEED:
                self.state = 'moveArm'
                # Publish.set_manipulator_action('rips_out')
                # Publish.set_neck(0, 0, 0)
        elif self.state == 'moveArm':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak(
                    "Hello Sir, My name is Lumyai. I came from Kasetsart University Thailand. I am a robot from planet earth, came here to service you. Please accept this registration.")
                self.state = 'waitForCommand'
        elif self.state == 'waitForCommand':
            if device == Devices.voice and data == 'leave apartment':
                self.state = 'armIn'
                # send to arm
                Publish.set_manipulator_action('walking')
        elif self.state == 'armIn':
            if device == Devices.manipulator and data == 'finish':
                # send to pan_tilt
                Publish.set_neck(0, 50 * pi / 180, 0)
                self.delay.delay(2)
                # send to base
                self.move_robot('outside_pos')
                self.state = 'getOut'
        elif self.state == 'getOut':
            Publish.set_neck(0, 50 * pi / 180, 0)
            Publish.set_manipulator_action('walking')
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'finish'


if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        RIPS()
    except Exception, error:
        print str(error)
