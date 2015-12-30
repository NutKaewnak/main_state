#!/usr/bin/env python
__author__ = "fpt-Rainnie"

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


def pick_tester():
    global mnplctrl
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('test_manipulator')

    mnplctrl.pickobject_init("right_arm", "object", [0.82, -0.13, 0.8])

    mnplctrl.manipulate('right_arm', [0.82, -0.13, 0.8])

if __name__ == '__main__':
    try:
        pick_tester()
    except rospy.ROSInterruptException:
        pass
