#!/usr/bin/env python
import rospy
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Bool, Float64
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import object_detection.msg
import tf
from dynamixel_controllers.srv import SetTorqueLimit
from controller.manipulator_controller import ManipulateController
from tabletop.srv import TabletopObjectDetection
import numpy
from controller_tester import *

__author__ = "Kandithws"

framecount = 0

mnplctrl = None
pos = []
pub = None
enable = False

finish = False


def robozoo_tester():
    global mnplctrl, finish

    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('robozoo')
    rospy.Subscriber("wip_done", Bool, boolcallback)

    rospy.loginfo('1st:right_init_picking')
    mnplctrl.static_pose('right_arm', "right_init_picking")
    rospy.loginfo('executing:right_init_picking')
    # raw_input()
    rospy.sleep(4.00)

    rospy.loginfo('2nd:right_pregrasp')
    mnplctrl.static_pose('right_arm', "right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    # raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('3rd:right_wip_prepare')
    mnplctrl.static_pose('right_arm', "right_wip_prepare")
    rospy.loginfo('executing:right_wip_prepare')
    # raw_input()
    rospy.sleep(4.00)

    # while not rospy.is_shutdown():
    while (not finish) and (not rospy.is_shutdown()):
        rospy.loginfo('wip1')
        mnplctrl.static_pose('right_arm', "right_wip_1")
        # raw_input()
        rospy.sleep(1.50)
        rospy.loginfo('wip2')
        mnplctrl.static_pose('right_arm', "right_wip_2")
        # raw_input()
        rospy.sleep(1.50)

    rospy.loginfo('4th : right_wip_retreat')
    mnplctrl.static_pose('right_arm', "right_wip_retreat")
    rospy.loginfo('executing:right_wip_retreat')
    # raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('5th : right_pregrasp')
    mnplctrl.static_pose('right_arm', "right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    # raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('6th : right_init_picking')
    mnplctrl.static_pose('right_arm', "right_init_picking")
    rospy.loginfo('--Finish--')

def test():
    global mnplctrl, finish
    rospy.init_node('robozoo')
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    
    #rospy.Subscriber("wip_done", Bool, boolcallback)
    rospy.loginfo('1st:right_init_picking')
    mnplctrl.static_pose('right_arm', "right_init_picking")


if __name__ == '__main__':
    try:
        test()
    except rospy.ROSInterruptException:
        pass
