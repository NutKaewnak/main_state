#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
import std_msgs.msg
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import object_detection.msg
import tf
from controller.manipulator_controller import ManipulateController

framecount = 0

mnplctrl = None

def callback(data):
    global framecount
    position = geometry_msgs.msg.Point()
    position = data.centriod
    framecount += 1
    print "msg counting " + str(framecount)

    if framecount is not 3:
        return
    rospy.loginfo('------------start  picking----------')
    print "location : x = " + str(position.x) + "  y= " + str(position.y) + " z= " + str(position.z) 
    mnplctrl.pick("right_arm",[position.x,position.y,position.z],[0.0,0.0,0.0],"object","table","base_link")
    #mnplctrl.robot.right_arm.set_support_surface_name("table")
    #mnplctrl.robot.right_arm.pick("object")






def tester():
    global mnplctrl
    
    
    mnplctrl = ManipulateController()
    print "hello"
    rospy.init_node('controller_tester')
    rospy.Subscriber("/object_shape", object_detection.msg.ObjectDetection, callback)
    mnplctrl.static_pose("right_arm","right_normal")
    #rospy.sleep(5)
    ##subscribing objects
    


    #print "-------start commanding rightarm------"
    #mnplctrl.manipulate("right_arm",[0.4,-0.3,0.6],[0,0,0],"base_link")

    #mnplctrl.pick("right_arm",[0.43,-0.15,0.5],[0,0,0],"object","table","base_link")
    #print "-----------finish pick----------"
    rospy.spin()
    mnplctrl.__del__()

if __name__=='__main__':
    try:
        tester()
    except rospy.ROSInterruptException:
        pass