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
        #self.robot_pos.append(0)
        #self.state = 'init'
        rospy.loginfo('Start Follow Me State')
        rospy.Subscriber("/base/base_pos", Pose2D, self.cb_base_pos)
        rospy.Subscriber("/scan/wall_people", Pose2D, self.cb_wall_people)
        self.robot_pos_wall = None
        self.publish = Publish()
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

    def cb_wall_people(self,data):
        pos_ = Pose2D()
        pos_.x = data.x + 1.5
        pos_.y = data.y + 0.5
        pos_.theta =3.14/2
        self.robot_pos_wall = pos_
        self.main(Devices.foot_detect,pos_)

    def main(self,device,data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:")
        if self.state == 'init':
#    global state,startTime
            if(device == Devices.voice and ('follow me' in data)):
                Publish.speak("I will follow you.")
                self.state = 'follow_phase_2'
        elif(self.state == 'follow_phase_1'):
            if(device == Devices.follow):
                if(data.text_msg == 'lost'):
                   # rospy.loginfo("robot_move" + data.x + data.y)
                    data.text_msg = 'stop'
                Publish.move_robot(data)
            #if(data.text_msg == 'stop'):
            #    data.text_msg = 'clear'
                        #    pub['base'].publish(data)
            elif(device == Devices.voice and ('leave the elevator' in data)):
                self.state = 'get_out_lift'
                Publish.move_absolute(self.robot_pos[0])
                #Publish.move_robot(NavGoalMsg('clear','absolute',self.robot_pos[0]))
        elif(self.state == 'get_out_lift'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 're_calibrate'
                self.speak("please come in front of me.")
        elif(self.state == 're_calibrate'):
            #if(delay.isWaitFinish()):
            self.publish.follow_init.publish(Bool(True))
            self.state = 'follow_phase_2'
        elif(self.state == 'follow_phase_2'):
            if(device == Devices.follow):
                if(data.text_msg == 'lost'):
                     data.text_msg = 'stop'
                               #pub['base'].publish(data)
                Publish.move_robot(data)
            elif(device == Devices.foot_detect):
                rospy.loginfo(type(data))
                rospy.loginfo(str(data))
                Publish.move_absolute(data)
                self.state = 're_calibrate_2'
                self.wait(3)
        elif(self.state == 're_calibrate_2'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.speak("please come in front of me.")
                self.publish.follow_init.publish(Bool(True))
                self.state = 'follow_phase_3'
        elif(self.state == 'follow_phase_3'):
            if(device == Devices.follow):
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
