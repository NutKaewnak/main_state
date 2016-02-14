#!/usr/bin/env python
__author__ = 'fptrainnie'


import rospy
from std_msgs.msg import Float64



# def respect():
#     global mnplctrl
#     rospy.loginfo('Lumyai Respect')
#     mnplctrl.static_pose('right_arm',"right_respect_1")
#     #rospy.sleep(4.00)
#     mnplctrl.static_pose('left_arm',"left_respect_1")
#     #rospy.sleep(4.00)
#     mnplctrl.static_pose('right_arm',"right_respect_2")
#     #rospy.sleep(2.00)
#     mnplctrl.static_pose('left_arm',"left_respect_2")
#     #rospy.sleep(2.00)

# def normal():
#     global mnplctrl
#     rospy.loginfo('Lumyai normal')
#     mnplctrl.static_pose('right_arm',"right_normal")
#     #rospy.sleep(5.00)
#     mnplctrl.static_pose('left_arm',"left_normal")
#     #rospy.sleep(5.00)

#pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)

# def normal():
#     pub1 = rospy.Publisher('/dynamixel/right_shoulder_1_controller/command',std_msgs/Float64)
#     pub1.Publish(std_msgs/Float64 "data: 0.0")

def free():
#    rospy.init_node('normal',anonymous=True)
    print 'saassssss'   
    global pub_sh1_r
    global pub_sh2_r
    global pub_elb_r
    global pub_wst1_r
    global pub_wst2_r
    global pub_wst3_r
    global pub_sh1_l
    global pub_sh2_l
    global pub_elb_l
    global pub_wst1_l
    global pub_wst2_l
    global pub_wst3_l
    pub_sh2_r.publish(0.0)
    pub_sh2_l.publish(0.0)    
    rospy.sleep(2.0)
    pub_sh1_r.publish(-0.1)
    pub_sh1_l.publish(0.15)
    pub_sh1_l.publish(0.1)
    rospy.sleep(0.5)
    pub_sh1_r.publish(-0.05)    
    pub_sh1_l.publish(0.05)
    rospy.sleep(0.5)

def normal():
#    rospy.init_node('normal',anonymous=True)
    print 'saassssss'   
    global pub_sh1_r
    global pub_sh2_r
    global pub_elb_r
    global pub_wst1_r
    global pub_wst2_r
    global pub_wst3_r
    global pub_sh1_l
    global pub_sh2_l
    global pub_elb_l
    global pub_wst1_l
    global pub_wst2_l
    global pub_wst3_l
    pub_elb_r.publish(0.0)
    pub_elb_l.publish(0.0)
    rospy.sleep(2.0)
    pub_sh1_r.publish(0.0)
    pub_sh1_l.publish(0.0)
    pub_wst1_r.publish(0.0)
    pub_wst1_l.publish(0.0)
    pub_wst2_r.publish(1.2)
    pub_wst2_l.publish(1.2)
    pub_wst3_r.publish(0.0)
    pub_wst3_l.publish(0.0)
    raw_input()

def respect():
    print 'cryyy' 
#    rospy.init_node('respect',anonymous=True)
    global pub_sh1_r
    global pub_sh2_r
    global pub_elb_r
    global pub_wst1_r
    global pub_wst2_r
    global pub_wst3_r
    global pub_sh1_l
    global pub_sh2_l
    global pub_elb_l
    global pub_wst1_l
    global pub_wst2_l
    global pub_wst3_l    
    pub_sh1_r.publish(-0.15)
    pub_sh1_l.publish(0.2)
    pub_elb_r.publish(0.3)
    pub_elb_l.publish(-0.2)
    rospy.sleep(2.0)
    pub_sh2_r.publish(0.32)
    pub_sh2_l.publish(-0.15)
    pub_wst1_r.publish(0.0)
    pub_wst1_l.publish(0.0)
    pub_wst2_r.publish(-0.8)
    pub_wst2_l.publish(-1.8)
    pub_wst3_r.publish(1.4)
    pub_wst3_l.publish(1.6)

def bye():
    print 'see ya'
    global pub_sh1_r
    global pub_sh2_r
    global pub_elb_r
    global pub_wst1_r
    global pub_wst2_r
    global pub_wst3_r
    global pub_sh1_l
    global pub_sh2_l
    global pub_elb_l
    global pub_wst1_l
    global pub_wst2_l
    global pub_wst3_l 
    pub_sh1_r.publish(-0.4)
    pub_sh2_r.publish(0.0)
    pub_elb_r.publish(0.3)
    pub_wst1_r.publish(0.0)
    pub_wst2_r.publish(0.0)
    pub_wst3_r.publish(0.0)
    pub_sh1_l.publish(0.0)
    pub_sh2_l.publish(0.0)
    pub_elb_l.publish(0.0)
    pub_wst1_l.publish(0.0)
    pub_wst2_l.publish(0.0)
    pub_wst3_l.publish(0.0)

    rospy.sleep(1.0)
    pub_sh2_r.publish(0.3)
    rospy.sleep(1.0)
    pub_sh2_r.publish(-0.3)
    rospy.sleep(1.0)
    pub_sh2_r.publish(0.3)
    rospy.sleep(1.0)
    pub_sh2_r.publish(-0.3)
    rospy.sleep(1.0)
    pub_sh2_r.publish(0.3)
    rospy.sleep(1.0)
    pub_sh2_r.publish(-0.3)
    rospy.sleep(1.0)

    pub_sh2_r.publish(0.0)
    normal()
    
def start():
    global pub_sh1_r
    global pub_sh2_r
    global pub_elb_r
    global pub_wst1_r
    global pub_wst2_r
    global pub_wst3_r
    global pub_sh1_l
    global pub_sh2_l
    global pub_elb_l
    global pub_wst1_l
    global pub_wst2_l
    global pub_wst3_l
    rospy.init_node('start',anonymous=True)
    pub_sh1_r = rospy.Publisher('/dynamixel/right_shoulder_1_controller/command',Float64,queue_size=10)
    pub_sh2_r = rospy.Publisher('/dynamixel/right_shoulder_2_controller/command',Float64,queue_size=10)
    pub_elb_r = rospy.Publisher('/dynamixel/right_elbow_controller/command',Float64,queue_size=10)
    pub_wst1_r = rospy.Publisher('/dynamixel/right_wrist_1_controller/command',Float64,queue_size=10)
    pub_wst2_r = rospy.Publisher('/dynamixel/right_wrist_2_controller/command',Float64,queue_size=10)
    pub_wst3_r = rospy.Publisher('/dynamixel/right_wrist_3_controller/command',Float64,queue_size=10)
    pub_sh1_l = rospy.Publisher('/dynamixel/left_shoulder_1_controller/command',Float64,queue_size=10)
    pub_sh2_l = rospy.Publisher('/dynamixel/left_shoulder_2_controller/command',Float64,queue_size=10)
    pub_elb_l = rospy.Publisher('/dynamixel/left_elbow_controller/command',Float64,queue_size=10)
    pub_wst1_l = rospy.Publisher('/dynamixel/left_wrist_1_controller/command',Float64,queue_size=10)
    pub_wst2_l = rospy.Publisher('/dynamixel/left_wrist_2_controller/command',Float64,queue_size=10)
    pub_wst3_l = rospy.Publisher('/dynamixel/left_wrist_3_controller/command',Float64,queue_size=10) 
    raw_input()        
    normal()
    raw_input()
    respect()
    raw_input()
    free()        
    normal()
    raw_input()
    bye()
    
if __name__ == '__main__':
    try:
        start()
    except rospy.ROSInterruptException:
        pass
