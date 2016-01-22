#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Bool,Float64
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import object_detection.msg
import tf
from dynamixel_controllers.srv import SetTorqueLimit
from controller.manipulator_controller import ManipulateController
from tabletop.srv import TabletopObjectDetection
import numpy

__author__ = 'ftprainnie'

framecount = 0
mnplctrl = None
pos = []
pub = None
enable = False
finish = False


def set_torque_limit(limit=0.5):
    rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
    try:
        rospy.loginfo('settorque')
        setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
        respTorque = setTorque(limit)
    except rospy.ServiceException, e:
        rospy.logwarn("Service Torque call failed " + str(e))

def pick_tester():
    global mnplctrl, pub, pos
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('controller_tester')

    pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
    pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)

    rospy.loginfo("---BUILDING SCENE----")
    rospy.sleep(3.0)

    rospy.loginfo("--INIT PICK NORMAL--")
    mnplctrl.pickobject_init("right_arm","object", [0.6, -0.18, 1.4])
    rospy.loginfo("Press any key to Continue")
    raw_input()
    
    rospy.loginfo("---PICK PREPARE---")
    mnplctrl.pickobject_prepare()
    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("---Opening Gripper---")
    #mnplctrl.pickobject_opengripper()
    pub_right_gripper.publish(1.1)
    #pub.publish(Float64(mnplctrl.GRIPPER_OPENED))

    rospy.loginfo("---Complete Opening Gripper----")

    rospy.loginfo("Press any key to Continue")
    raw_input()    
    rospy.loginfo("---PREGRASP---")
    mnplctrl.pickobject_pregrasp()
    rospy.loginfo("Press any key to Continue")
    raw_input()
    
    rospy.loginfo("----movetoobjectfront v1----")
    mnplctrl.pickobject_movetoobjectfront_1()
    rospy.loginfo("movetoobjectfront Complete")

    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("----movetoobjectfront v2----")
    mnplctrl.pickobject_movetoobjectfront_2()
    rospy.loginfo("movetoobjectfront Complete")

    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("----movetoobjectfront v3----")
    mnplctrl.pickobject_movetoobjectfront_3()
    rospy.loginfo("movetoobjectfront Complete")

    rospy.loginfo("Press any key to Continue")
    raw_input()

    #rospy.loginfo("----Reaching to Object----")
    #mnplctrl.pickobject_reach()
    #rospy.loginfo("Reaching Complete")

    #rospy.loginfo("Press any key to Continue")
    #raw_input()
    
    rospy.loginfo("---GRASPING---")
    #mnplctrl.pickobject_grasp()
    
    set_torque_limit()
    pub_right_gripper.publish(0.3)
    pub_right_wrist_2.publish(0.0)
    # mnplctrl.pickobject_movetoobjectfront_2()
    #pub.publish(Float64(mnplctrl.GRIPPER_CLOSED))

    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("---After Grasp---")
    # mnplctrl.pickobject_after_grasp()

    # rospy.loginfo("Press any key to Continue")
    # raw_input()

    # rospy.loginfo("---pregrasp---")
    mnplctrl.pickobject_prepare()
    rospy.loginfo("Press any key to Continue")
    raw_input()

    # rospy.loginfo("----Return To Normal-----")
    # mnplctrl.static_pose("right_arm","right_init_picking")
    # rospy.loginfo("---FINISH----")
    # raw_input()
    # rospy.loginfo("---Opening Gripper---")
    #mnplctrl.pickobject_opengripper()

    # pub.publish(Float64(mnplctrl.GRIPPER_OPENED))

    # rospy.loginfo("---Complete Opening Gripper----")

    # rospy.spin()
    # mnplctrl.__del__()


if __name__ == '__main__':
    global callback
    try:
        pick_tester()
    except rospy.ROSInterruptException:
        pass
