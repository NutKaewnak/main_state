#!/usr/bin/env python
import rospy
import roslib
import time
from subprocess import call

roslib.load_manifest('main_state')

from std_msgs.msg import String
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D, Vector3

state = 'init'
#state = 'getCommand'
pub = {}
living_room = NavGoalMsg('clear', 'absolute', Pose2D(1.682, 3.214, 0.647))
table_pos = NavGoalMsg('clear', 'absolute', Pose2D(-4.805, 10.542, 2.490))
startTime = 0
current_pos = 0
objectName = ''
peopleName = ''
temp = []


def cb_door(data):
    main_state('door', data.data)


def cb_voice(data):
    main_state('voice', data.data)


def cb_manipulator(data):
    main_state('manipulator', data.data)


def cb_gesture(data):
    main_state('gesture', data.data)


def cb_base(data):
    main_state('base', data.data)


def main_state(device, data):
    global state, pub, startTime, current_pos, objectName, peopleName, temp
    rospy.loginfo("state:" + state + " from:" + device + " " + data)
    if (state == 'init'):
        if (device == 'gesture'):
            state = 'gotoIk'
            x, y, z = data.split(',')
            # send to base
            pub["base"].publish(NavGoalMsg('clear', 'relative', Pose2D(float(x), float(y), 0.0)))
    elif (state == 'gotoIk'):
        if (device == 'base' and data == 'SUCCEEDED'):
            call(['espeak', 'i will waving fan for you', '-ven+f4', '-s 150'])
            state = 'waving'
    elif (state == 'waving'):
        pub['manipulator'].publish(String('fan_wave'))
        if (device == 'voice' and ('stop' in data)):
            pub['manipulator'].publish(String('show_lift'))
            state = 'waitForCommand'
    elif (state == 'waitForCommand'):
        if (device == 'voice' and ('take out' in data)):
            call(['espeak', 'i will take it out', '-ven+f4', '-s 150'])
            pub["base"].publish(NavGoalMsg('clear', 'absolute', Pose2D(-2.906, -1.140, -2.172)))
            state = 'getOut'
    elif (state == 'getOut'):
        if (device == 'base' and data == 'SUCCEEDED'):
            state = 'Fin'


def main():
    pub['base'] = rospy.Publisher('/base/set_pos', NavGoalMsg)
    #pub['object_point'] = rospy.Publisher('/object_point', Vector3)
    pub['manipulator'] = rospy.Publisher('/manipulator/action', String)
    #pub['start_search'] = rospy.Publisher('/object/start_search', String)
    rospy.init_node('main_state')
    #rospy.Subscriber("/door/is_open", String, cb_door)
    rospy.Subscriber("/base/is_fin", String, cb_base)
    #rospy.Subscriber("/manipulator/is_fin", String, cb_manipulator)
    rospy.Subscriber("/gesture/point", String, cb_gesture)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
