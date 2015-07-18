#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Bool
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import object_detection.msg
import tf
from controller.manipulator_controller import ManipulateController

framecount = 0

mnplctrl = None
pos = []
pub = None
enable = False

finish = False

def callback(data):
    global framecount,enable,pos
    position = geometry_msgs.msg.Point()
    position = data.centriod
    framecount += 1
    if framecount < 5:
        #print "msg counting " + str(framecount)
        return
    if framecount is 5:
        enable = True
        rospy.loginfo('------------start  picking----------')
        print "location : x = " + str(position.x) + "  y= " + str(position.y) + " z= " + str(position.z) 
        pos.append(position.x)
        pos.append(position.y)
        pos.append(position.z)
    #mnplctrl.pick("right_arm",[position.x-0.2,position.y,position.z+0.05],[0.0,0.0,0.0],"object","table","base_link")
    #mnplctrl.robot.right_arm.set_support_surface_name("table")
    #mnplctrl.robot.right_arm.pick("object")
    #moveit_commander.


def adding_fake_object():
    global mnplctrl,pub
    ##publishing object
    mnplctrl.scene.remove_world_object("pole")
    mnplctrl.scene.remove_world_object("table")
    mnplctrl.scene.remove_world_object("object")

    # publish a demo scene
    p = geometry_msgs.msg.PoseStamped()
    p.header.frame_id = 'base_link'
    p.pose.position.x = 0.7
    p.pose.position.y = 1
    p.pose.position.z = 0.85
    p.pose.orientation.w = 1.0
    mnplctrl.scene.add_box("pole", p, (0.3, 0.1, 1.0))
    p.pose.position.x = 0.725
    p.pose.position.y = -0.2
    p.pose.position.z = 0.175
    mnplctrl.scene.add_box("table", p, (0.5, 1.5, 0.35))

    p.pose.position.x = 0.7
    p.pose.position.y = 0
    p.pose.position.z = 0.5
    mnplctrl.scene.add_box("object", p, (0.15, 0.06, 0.3))
    


def pick_tester():
    global mnplctrl,pub,pos
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('controller_tester')
    #pub = rospy.Publisher('collision_object', moveit_msgs.msg.CollisionObject, queue_size=10)
    #raw_input()
    rospy.loginfo("---BUILDING SCENE----")
    # rospy.sleep(5)
    # mnplctrl.scene.remove_world_object("pole")
    # mnplctrl.scene.remove_world_object("table")
    # mnplctrl.scene.remove_world_object("object")

    # adding_fake_object()
    #rospy.sleep(2)
    rospy.sleep(3.0)
    rospy.loginfo("--INIT--")
    mnplctrl.pickobject_init("right_arm", "object", [0.58, -0.03, 0.90])
    #mnplctrl.static_pose("right_arm","right_normal")
    #mnplctrl.static_pose("right_arm","right_init_picking")
    rospy.loginfo("Press any key to Continue")
    raw_input()
    #rospy.loginfo("--Walking--")
    #mnplctrl.static_pose("right_arm","right_walking")
    #mnplctrl.static_pose("left_arm","left_normal")
    #rospy.sleep(15)

    #rospy.loginfo("Complete Normal")
    #rospy.Subscriber("/object_shape", object_detection.msg.ObjectDetection, callback)
    #while enable is False:
    #    pass
        
    #rospy.loginfo("Starting manipulation")
    #mnplctrl.pickobject_pregrasp("right_arm","object",[pos[0],pos[1],pos[2]])
    #mnplctrl.pickobject_pregrasp("right_arm","object",[0.62,0.0,0.95])
    
    #mnplctrl.pickobject_pregrasp("right_arm","object",[0.78-0.07,0.00 + 0.03,0.78+0.33]) #pringgle
    rospy.loginfo("---pregrasp---")
    #mnplctrl.pickobject_pregrasp("right_arm","object",[0.58,-0.03,0.90])

    #mnplctrl.pickobject_pregrasp_planB("right_arm", "object", [0.58, -0.03, 0.90])
    mnplctrl.pickobject_pregrasp_planB()

    #rospy.loginfo("Complete manipulation")
    rospy.loginfo("Press any key to Continue")
    raw_input()
    
    rospy.loginfo("---Opening Gripper---")
    mnplctrl.pickobject_opengripper()
    rospy.loginfo("---Complete Opening Gripper----")


    rospy.loginfo("Press any key to Continue")
    raw_input()
    
    rospy.loginfo("----Reaching to Object----")
    # mnplctrl.pickobject_reach([0.1,0.2])
    mnplctrl.pickobject_reach()
    rospy.loginfo("Reaching Complete")

    rospy.loginfo("Press any key to Continue")
    raw_input()
    rospy.loginfo("---GRASPING---")
    
    mnplctrl.pickobject_grasp()
    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("---After Grasp---")
    mnplctrl.pickobject_after_grasp()

    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("----Return To Normal-----")
    #mnplctrl.static_pose("right_arm", "right_normal")
    mnplctrl.static_pose("right_arm","right_init_picking")
    rospy.loginfo("---FINISH----")
    # print "-----start----"
    # Manually pick in simulation
    # mnplctrl.pick("right_arm",[0.50,-0.15,0.55],[0.0,0.0,0.0],"object","table","base_link")

    # print "-----------finish pick----------"
    rospy.spin()
    mnplctrl.__del__()

def module_tester():

    global mnplctrl
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('controller_tester')
    rospy.sleep(3.0)
    rospy.loginfo(  str( mnplctrl.getjointstatus('right_arm')  ))
    rospy.spin()

def boolcallback(data):
    global finish
    if data.data == True:
        rospy.loginfo('---ENDING WIP---')
        finish = True
    else:
        rospy.loginfo('Wrong input')


def robozoo_tester():
    global mnplctrl,finish

    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('robozoo')
    rospy.Subscriber("wip_done", Bool, boolcallback)

    rospy.loginfo('1st:right_init_picking')
    mnplctrl.static_pose('right_arm',"right_init_picking")
    rospy.loginfo('executing:right_init_picking')
    #raw_input()
    rospy.sleep(4.00)

    rospy.loginfo('2nd:right_pregrasp')
    mnplctrl.static_pose('right_arm',"right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    #raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('3rd:right_wip_prepare')
    mnplctrl.static_pose('right_arm',"right_wip_prepare")
    rospy.loginfo('executing:right_wip_prepare')
    #raw_input()
    rospy.sleep(4.00)
    
    #while not rospy.is_shutdown():
    while not finish:
        rospy.loginfo('wip1')
        mnplctrl.static_pose('right_arm',"right_wip_1")
        #raw_input()
        rospy.sleep(1.50)
        rospy.loginfo('wip2')
        mnplctrl.static_pose('right_arm',"right_wip_2")
        #raw_input()
        rospy.sleep(1.50)

    rospy.loginfo('4th : right_wip_retreat')
    mnplctrl.static_pose('right_arm',"right_wip_retreat")
    rospy.loginfo('executing:right_wip_retreat')
    #raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('5th : right_pregrasp')
    mnplctrl.static_pose('right_arm',"right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    #raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('6th : right_init_picking')
    mnplctrl.static_pose('right_arm',"right_init_picking")
    rospy.loginfo('--Finish--')
   
        

        



if __name__=='__main__':
    try:
        #pick_tester()
        #module_tester()
        robozoo_tester()

    except rospy.ROSInterruptException:
        pass