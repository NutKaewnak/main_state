__author__ = 'nicole'
import rospy
import math
from include.base_state import *
from factory.move import Move

class followme_v2(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.robot_pos = []
        rospy.loginfo('Start Follow Me State')
        rospy.Subscriber("/base/base_pos", Pose2D, self.cb_base_pos)

    def cb_base_pos(self, data):
        pos = data
        if len(self.robot_pos) == 0:
            self.robot_pos.append(pos)
        else:
            last_pos = self.robot_pos[-1]
        dif = math.sqrt((last_pos.x-pos.x)**2 + (last_pos.y-pos.y)**2)
        if dif >= 0.15:
            self.robot_pos.append(pos)
        temp = self.robot_pos
        for _pos in self.robot_pos:
            dif = math.sqrt((_pos.x-pos.x)**2 + (_pos.y-pos.y)**2)
            if dif >= 2.3:
                temp = temp[1:]
        self.robot_pos = temp

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:")
        if self.state is STATE.INIT:
            self.changeStateTo(STATE.WAITING)
        elif self.state is STATE.WAITING:
            if device is Devices.voice and ('follow me' in data):
                Publish.speak("I will follow you.")
                Move.follow().start()
                self.changeStateTo(STATE.FOLLOWING)

        elif self.state is STATE.FOLLOWING:
            if device is Devices.voice and any(s in data for s in ['stop', 'halt', 'halting', 'wait']):
                if 'halt' in data or 'halting' in data or 'wait' in data:
                    Move.follow().stop(STATE.WAITING)
                    self.changeStateTo(STATE.WAITING)
                else:
                    Move.follow().stop(STATE.ABORTED)

        elif self.state is STATE.FOLLOWING:
            if device is Devices.voice and 'leave the elevator' in data:
                self.speak("i will get out elevator")
                self.state = 'get_out_lift'
                Move.moveToLocation().to(self.robot_pos[0])

        elif self.state == 'get_out_lift':
            Move.follow().changeStateTo('re_calibrate')

if __name__ == '__main__':
    followme_v2()

