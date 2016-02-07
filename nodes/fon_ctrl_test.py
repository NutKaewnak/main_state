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
from geometry_msgs.msg import Vector3
from inverseKinematic import inverseKinematics

__author__ = 'ftprainnie'

framecount = 0
mnplctrl = None
pos = []
pub = None
enable = False
finish = False


class PointToPick():

    def __init__(self):
        # self.receive_point()
        self.pick_tester()

    def set_torque_limit(self, limit = 0.3):
        rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
        try:
            rospy.loginfo('settorque')
            setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
            respTorque = setTorque(limit)
        except rospy.ServiceException, e:
            rospy.logwarn("Service Torque call failed " + str(e))

    pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
    pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)


    def pick_tester(self):
        global mnplctrl,pub,pos
        mnplctrl = ManipulateController()
        mnplctrl.init_controller()
        invK = inverseKinematics()
        object_pos = [0.710445 -0.05, -0.230658 + 0.11, 0.786225 + 0.05]

        pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
        pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)
        pub_right_wrist_3 = rospy.Publisher('/dynamixel/right_wrist_3_controller/command', Float64)
        pub_tilt = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        pub_pan = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        pub_prismatic = rospy.Publisher('/dynamixel/prismatic_controller/command', Float64)

        rospy.loginfo("---BUILDING SCENE----")
        rospy.sleep(3.0)

        rospy.loginfo("--INIT PICK NORMAL--")

        mnplctrl.pickobject_init("right_arm", "object", [0,0,0])
        # mnplctrl.pickobject_init("right_arm", "object", data)
        pub_pan.publish(0.0)
        pub_tilt.publish(-0.3)
        rospy.loginfo("Press any key to Continue")
        raw_input()

        rospy.loginfo("---Moving Up---")
        pub_prismatic.publish(0 + 0.23)
        rospy.loginfo("Press any key to Continue")
        raw_input()

        rospy.loginfo("---PICK PREPARE---")
        mnplctrl.pickobject_prepare()
        rospy.loginfo("Press any key to Continue")
        raw_input()

        rospy.loginfo("---Opening Gripper---")
        pub_right_gripper.publish(1.1)
        rospy.loginfo("---Complete Opening Gripper----")
        rospy.loginfo("Press any key to Continue")
        raw_input()

        rospy.loginfo("---PREGRASP---")
        mnplctrl.pickobject_pregrasp(object_pos)
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
        pub_right_wrist_2.publish(-0.2)
        rospy.loginfo("Press any key to Continue")
        raw_input()

        rospy.loginfo("----movetoobjectfront v3----")
        mnplctrl.pickobject_movetoobjectfront_3()
        rospy.loginfo("movetoobjectfront Complete")
        rospy.sleep(2.0)
        pub_right_wrist_2.publish(-0.2)
        
        rospy.loginfo("Press any key to Continue")
        raw_input()

        # rospy.loginfo("----Reaching to Object----")
        # mnplctrl.pickobject_reach()
        # rospy.loginfo("Reaching Complete")

        # rospy.loginfo("Press any key to Continue")
        # raw_input()

        # self.angle = invK.invKinematic(object_pos[0], object_pos[1], object_pos[2])
        # mnplctrl.movejoint('right_shoulder_1_joint', -1*self.angle[0])
        # mnplctrl.movejoint('right_shoulder_2_joint', self.angle[1])
        # mnplctrl.movejoint('right_elbow_joint', self.angle[2])
        # mnplctrl.movejoint('right_wrist_1_joint', self.angle[3])
        # mnplctrl.movejoint('right_wrist_2_joint', self.angle[4])
        # mnplctrl.movejoint('right_wrist_3_joint', self.angle[5])        

        rospy.loginfo("---GRASPING---")
        #mnplctrl.pickobject_grasp()

        self.set_torque_limit()
        pub_right_gripper.publish(-0.6)
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


    def receive_point(self):
        rospy.init_node('receive_point', anonymous = True)
        rospy.Subscriber("/object_point", Vector3, self.pick_tester)
        rospy.spin()


if __name__=='__main__':
    # global callback
    try:
        PointToPick()
    except rospy.ROSInterruptException:
        pass
