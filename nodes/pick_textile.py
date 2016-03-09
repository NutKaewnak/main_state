#!/usr/bin/env python
import rospy
from controller.manipulator_controller import ManipulateController
from skill.include import inverse_kinematics
from task.include.delay import Delay
from geometry_msgs.msg import Point


__author__ = 'fptrainnie'


class PickTextile:
    def __init__(self):
        global invK, manipulator_ctrl
        self.delay = Delay()
        rospy.init_node('pick_textile')
        invK = inverse_kinematics.InverseKinematics()
        manipulator_ctrl = ManipulateController()
        self.invKine()

    def invKine(self):


if __name__ == '__main__':
    try:
        PickTextile()
    except rospy.ROSInterruptException:
        pass
