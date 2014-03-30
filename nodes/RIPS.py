#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from math import pi

roslib.load_manifest('main_state')

class RIPS(BaseState):
    def __init__(self):
        BaseState.__init__(self)

        Publish.set_height(1.27)
        rospy.loginfo('Start RIPS State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if self.state == 'init':
            if device == Devices.door and data == 'open':
                # move pass door
                Publish.move_relative(1.5, 0)
                self.state = 'passDoor'
            Publish.set_neck(0, 50*pi/180,0)
            Publish.set_manipulator_action('walking')
        elif self.state == 'passDoor':
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'gotoTable'
                # send to base
                self.move_robot('register_pos')
        elif self.state == 'goToTable':
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'moveArm'
                # send to arm
                Publish.set_manipulator_action('rips_out')
                Publish.set_neck(0, 0, 0)
        elif self.state == 'moveArm':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("Hello Sir, My name is Lumyai. I came from Kasetsart University Thailand. I am a robot from planet earth, came here to service you. Please accept this registration.")
                self.state = 'waitForCommand'
        elif self.state == 'waitForCommand':
            if self.device == Devices.voice and data == 'leave apartment':
                self.state = 'armOut'
                # send to arm
                Publish.set_manipulator_action('walking')
        elif self.state == 'armOut':
            if device == Devices.manipulator and data == 'finish':
                # send to pan_tilt
                Publish.set_neck(0, 50*pi/180, 0)
                self.delay.delay(2)
                # send to base
                self.move_robot('outside_pos')
                self.state = 'getOut'
        elif self.state == 'getOut':
            Publish.set_neck(0, 50*pi/180,0)
            Publish.set_manipulator_action('walking')
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'finish'


if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        RIPS()
    except Exception, error:
        print str(error)
