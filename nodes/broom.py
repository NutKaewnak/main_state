#!/usr/bin/env python
__author__ = 'fptrainnie'


import rospy
from std_msgs.msg import Float64
from controller.manipulator_controller import ManipulateController 

class Maid:
    def __init__(self):
        rospy.init_node('broom',anonymous=True)
        self.mnplctrl = ManipulateController()
        self.mnplctrl.init_controller()

    def pick(self):
        rospy.loginfo('1st: right_left_normal')
        self.mnplctrl.static_pose('right_arm',"right_normal")
        rospy.sleep(2.00)
        self.mnplctrl.static_pose('left_arm',"left_normal")
        rospy.sleep(2.0)
        raw_input()

        rospy.loginfo('2nd: left_sweep')
        self.mnplctrl.static_pose('left_arm',"left_sweep")
        rospy.sleep(3.00)

        rospy.loginfo('3nd: right_pick_broom')
        self.mnplcrtl.static_pose('right_arm',"right_arm_pick_broom")
        rospy.sleep(3.00)
        self.mnplctrl.static_pose('right_gripper',"right_gripper_pick_broom")



if __name__ == '__main__':
#    if __package__ is None:
#        from os import sys, path
#        sys.path.append(path.dirname(path.dirname(path.abspath('.'))))
    try:
        a = Maid()  
    except rospy.ROSInterruptException:
        print str(error)
