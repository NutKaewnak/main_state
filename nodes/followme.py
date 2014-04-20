#!/usr/bin/env python
import rospy
import roslib
import time
import math
from subprocess import call
roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.base_state import *

from std_msgs.msg import String,Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D

class followme(BaseState):
    
    def __init__(self):
        BaseState.__init__(self)
        self.robot_pos = []
        self.robot_pos.append(0)
        #self.state = 'init'
        rospy.loginfo('Start Follow Me State')
        rospy.Subscriber("/base/base_pos", Pose2D, self.cb_base_pos)
        rospy.spin()

    def cb_base_pos(self,data):
        pos = data
        if(len(self.robot_pos) == 0):
            self.robot_pos.append(pos)
        else:
            last_pos = self.robot_pos[-1]
            dif = math.sqrt((last_pos.x-pos.x)**2 + (last_pos.y-pos.y)**2)
            if(dif >= 0.15):
                self.robot_pos.append(pos)
        temp = self.robot_pos
        for _pos in self.robot_pos:
            dif = math.sqrt((_pos.x-pos.x)**2 + (_pos.y-pos.y)**2)
            if(dif >= 2.0):
                temp = temp[1:]
        self.robot_pos = temp
    
    
    def main(self,device,data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if self.state == 'init' :
#    global state,startTime
            if(device == Devices.voice and ('follow me' in data)):
                Publish.speak("I will follow you.")
                self.state = 'follow_phase_1'
        elif(self.state == 'follow_phase_1'):
            if(device == Devices.follow):
                if(data.text_msg == 'lost'):
                    data.text_msg = 'stop'
                Publish.move_robot(data)
            #if(data.text_msg == 'stop'):
            #    data.text_msg = 'clear'
                        #    pub['base'].publish(data)
            elif(device == Devices.voice and ('get out' in data)):
                self.state = 'get_out_lift'
                Publish.move_absolute(self.robot_pos[0])
                #Publish.move_robot(NavGoalMsg('clear','absolute',self.robot_pos[0]))
        elif(self.state == 'get_out_lift'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 're_calibrate'
                Publish.speak("please come in front of me.")
                self.delay.waiting(5)
        elif(self.state == 're_calibrate'):
            if(self.delay.isWaitFinish()):
                self.state = 'follow_phase_2'
                publish.follow_init.publish(Bool(True))
            
            elif(self.state == 'follow_phase_2'):
                if(device == Devices.follow):
                    if(data.text_msg == 'lost'):
                        data.text_msg = 'stop'
                               #pub['base'].publish(data)
                    Publish.move_robot(data)


#state = 'init'
#self.robot_pos = []
#startTime = 0

#def cb_voice(data):
#    main_state('voice',data.data)

#def cb_base(data):
#    main_state('base',data.data)

#def cb_follow(data):
#    main_state('follow',data)


#def main():
#    rospy.init_node('main_state')
#    rospy.Subscriber("/base/is_fin", String, cb_base)
#    rospy.Subscriber("/follow/point", NavGoalMsg, cb_follow)
#    rospy.Subscriber("/base/base_pos", Pose2D, cb_base_pos)
#    rospy.Subscriber("/voice/output", String, cb_voice)
#    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        followme()
    except rospy.ROSInterruptException:
        pass
