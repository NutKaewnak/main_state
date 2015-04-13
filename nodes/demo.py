#!/usr/bin/env python
import rospy
import roslib
import time
from subprocess import call

roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.reconfig_kinect import *
from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Quaternion, Pose2D
from math import pi

state = 'init'
location_list = {}


def cb_door(data):
    main_state('door', data.data)


def cb_voice(data):
    main_state('voice', data.data)


def cb_manipulator(data):
    main_state('manipulator', data.data)


def cb_base(data):
    main_state('base', data.data)


def main_state(device, data):
    global state
    if delay.isWait(): return None
    rospy.loginfo("state:" + state + " from:" + device + " " + data)
    if state == 'init':
        state = 'waitForCommand'
        delay.delay(5)
        call(["espeak", "-ven+f4", "Welcome back Master, I'm on your right handside. How can i help you?", "-s 150"])
        delay.delay(3)

    elif state == 'waitForCommand':
        if device == 'voice':
            if 'kitchen' in data:
                call(["espeak", "-ven+f4", "I will lead to Kitchen, Follow me.", "-s 150"])
                # send to base
                publish.pan_tilt_command(getQuaternion(0, 0, 0))
                delay.delay(2)

                delay.waiting(4)
                publish.base.publish(location_list['kitchen'])
                state = 'gotoKitchen'
    elif state == 'gotoKitchen':
        if device == 'base' and data == 'SUCCEEDED':
            call(["espeak", "-ven+f4", "We arrived at the Kitchen", "-s 150"])
            state = 'waitForCommand2'
        elif delay.isWaitFinish():
            delay.waiting(10)
            call(["espeak", "-ven+f4", "Heading to Kitchen Follow me", "-s 150"])
    elif state == 'waitForCommand2':
        if device == 'voice':
            if 'living room' in data:
                call(["espeak", "-ven+f4", "I will lead to living room, Follow me.", "-s 150"])
                # send to base
                publish.pan_tilt_command(getQuaternion(0, 0, 0))
                delay.delay(2)

                delay.waiting(4)
                publish.base.publish(location_list['living room'])
                state = 'gotoLivingRoom'
    elif state == 'gotoLivingRoom':
        if device == 'base' and data == 'SUCCEEDED':
            call(["espeak", "-ven+f4", "We arrived at the Living Room", "-s 150"])
            state = 'waitForCommand'
        elif delay.isWaitFinish():
            delay.waiting(10)
            call(["espeak", "-ven+f4", "Heading to Living Room Follow me", "-s 150"])


def main():
    rospy.loginfo('Start Main_state')
    rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/voice/output", String, cb_voice)
    # rospy.Subscriber("/diagnostics", DiagnosticArray, cb_servo)
    publish.height_command(1.17)
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        delay = Delay()
        publish = Publish()
        reconfig = Reconfig()
        readLocation(location_list, '/config/location.txt')
        main()
    except rospy.ROSInterruptException:
        pass
