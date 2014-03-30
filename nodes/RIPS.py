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
        elif self.state == 'gotoTable':
            if device == Devices.base and data == 'SUCCEEDED':
                state = 'moveArm'
                # send to arm
                Publish.set_manipulator_action('rips_out')
                Publish.set_neck(0, 0, 0)
                Publish.speak("Hello Sir, My name is Lumyai. I came from Kasetsart University Thailand. I am a robot from planet earth, came here to service you. Please accept this registration.")
        elif (state == 'moveArm'):
            if (device == 'manipulator' and data == 'finish'):
                state = 'waitForCommand'

        elif (state == 'waitForCommand'):
            if (device == 'voice'):
                if (data == 'get out'):
                    state = 'arm out'
                    # send to arm
                    publish.manipulator_action.publish(String('walking'))
        elif (state == 'arm out'):
            if (device == 'manipulator' and data == 'finish'):
                # send to pan_tilt
                publish.pan_tilt_command(getQuaternion(0, 50 * pi / 180, 0))
                delay.delay(2)
                # send to base
                publish.base.publish(location_list['outside_pos'])
                state = 'get out'

        elif (state == 'set neck'):
            if (device == 'servo' and data == 'finish'):
                # send to base
                publish.base.publish(location_list['outside_pos'])
                state = 'get out'
        elif (state == 'get out'):
            publish.pan_tilt_command(getQuaternion(0, 50 * pi / 180, 0))
            publish.manipulator_action.publish(String('walking'))
            if (device == 'base' and data == 'SUCCEEDED'):
                state = 'finish'


if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        RIPS()
    except Exception, error:
        print str(error)
