#!/usr/bin/env python


import rospy
import math
from controller.inverseKinematics import InverseKinematics
from controller.manipulator_controller import ManipulateController
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool,Float64
from dynamixel_controllers.srv import SetTorqueLimit


__author__ = 'fptrainnie'


class test_invKine():

    def __init__(self):
        global invK, mnplctrl
        rospy.init_node('inverseKinematic')
        mnplctrl = ManipulateController()
        mnplctrl.init_controller()
        invK = InverseKinematics()
        self.invKine()
        rospy.sleep(2)

    pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)

    def set_torque_limit(self, limit = 0.3):
        rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
        try:
            rospy.loginfo('settorque')
            setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
            respTorque = setTorque(limit)
        except rospy.ServiceException, e:
            rospy.logwarn("Service Torque call failed " + str(e))

    def invKine(self):
        object_pos = [0.68, -0.21, 0.79] # [0.57, -0.07, 0.85]
        pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
        pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)
        pub_tilt = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        pub_pan = rospy.Publisher('/dynamixel/pan_controller/command', Float64)

        invK.init_position(object_pos[0],object_pos[1],object_pos[2],)
        # rospy.loginfo("---BUILDING SCENE----")
        # rospy.sleep(3.0)

        # rospy.loginfo("--INIT PICK NORMAL--")

        mnplctrl.pickobject_init("right_arm", "object", [0,0,0])
        # mnplctrl.pickobject_init("right_arm", "object", data)
        pub_pan.publish(0.0)
        pub_tilt.publish(-0.3)
        rospy.loginfo("Press any key to Continue")
        raw_input()

        rospy.loginfo("---PICK PREPARE---")
        angle = invK.inv_kinematic()

        r_sh1 = invK.inBound('right_shoulder_1_joint', -1*angle[0])
        mnplctrl.movejoint('right_shoulder_1_joint', r_sh1)
        r_sh2 = invK.inBound('right_shoulder_2_joint', -1*angle[1])
        mnplctrl.movejoint('right_shoulder_2_joint', r_sh2)
        r_elb = invK.inBound('right_elbow_joint', -1*angle[2])
        mnplctrl.movejoint('right_elbow_joint', r_elb)
        r_wr1 = invK.inBound('right_wrist_1_joint', angle[3])
        mnplctrl.movejoint('right_wrist_1_joint', r_wr1)
        r_wr2 = invK.inBound('right_wrist_2_joint', angle[4])
        mnplctrl.movejoint('right_wrist_2_joint', r_wr2)
        r_wr3 = invK.inBound('right_wrist_3_joint', angle[5])
        mnplctrl.movejoint('right_wrist_3_joint', r_wr3)

        rospy.loginfo("Press any key to Continue")
        raw_input()

        # rospy.loginfo("---Opening Gripper---")
        # mnplctrl.pickobject_opengripper()
        # # pub_right_gripper.publish(1.1)
        # # #pub.publish(Float64(mnplctrl.GRIPPER_OPENED))

        # rospy.loginfo("---Complete Opening Gripper----")

        # rospy.loginfo("Press any key to Continue")
        # raw_input()
        rospy.loginfo("---INVERSE KINEMATICS---")
        angle = invK.inv_kinematic(object_pos[0], object_pos[1], object_pos[2])

        r_sh1 = invK.inBound('right_shoulder_1_joint', -1*angle[0])
        mnplctrl.movejoint('right_shoulder_1_joint', r_sh1)
        r_sh2 = invK.inBound('right_shoulder_2_joint', -1*angle[1])
        mnplctrl.movejoint('right_shoulder_2_joint', r_sh2)
        r_elb = invK.inBound('right_elbow_joint', -1*angle[2])
        mnplctrl.movejoint('right_elbow_joint', r_elb)
        r_wr1 = invK.inBound('right_wrist_1_joint', angle[3])
        mnplctrl.movejoint('right_wrist_1_joint', r_wr1)
        r_wr2 = invK.inBound('right_wrist_2_joint', angle[4])
        mnplctrl.movejoint('right_wrist_2_joint', r_wr2)
        r_wr3 = invK.inBound('right_wrist_3_joint', angle[5])
        mnplctrl.movejoint('right_wrist_3_joint', r_wr3)
        
        # rospy.loginfo("Press any key to Continue")
        # raw_input()

        # rospy.loginfo("---GRASPING---")
        
        # self.set_torque_limit()
        # mnplctrl.pickobject_grasp()

        # rospy.loginfo("Press any key to Continue")
        # raw_input()

        # rospy.loginfo("---After Grasp---")
        
        # mnplctrl.pickobject_prepare()
        # rospy.loginfo("Press any key to Continue")
        # raw_input()


if __name__ == '__main__':
    try:
        test_invKine()
    except rospy.ROSInterruptException:
        pass
