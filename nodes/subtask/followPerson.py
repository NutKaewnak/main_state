__author__ = 'nicole'
import rospy
import math
from include.delay import Delay
from include.publish import Publish
from include.base_state import Devices, BaseState, STATE
from factory.neck import *
from factory.move import *

class FollowPerson(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.robot_pos = []
        self.currentAngle = -90*math.pi/180
        self.state = STATE.WAITING

    def cb_gesture(self, data):
        print "in cb_gesture cb"
        self.main('gesture', "%f,%f,%f" % (data.point.x, data.point.y, data.point.z))


    def main(self, device, data):
        if self.state is STATE.INIT:
            # Recognise people here
            self.changeStateTo(STATE.FOLLOWING)

        elif self.state == STATE.FOLLOWING:
            if device == Devices.follow:
                if data.text_msg == 'lost':
                    self.speak("I lost master")
                    data.text_msg = 'stop'
                Move.toLocation().toLocation(data)
            elif device == Devices.foot_detect:
                rospy.loginfo(type(data))
                rospy.loginfo(str(data))
                Publish.move_absolute(data)
                Neck.lookStraigth()
                self.currentAngle = -90*math.pi/180
                self.timer = Delay()
                self.changeStateTo('Seachgesture')
                self.speak("Please wave your hand.")
                self.wait(6)

        elif self.state == 'Seachgesture':
            if device == 'gesture':
                self.speak("I see you.")
                x, y, z = data.split(',')
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                Move.relative().to(float(x), float(y), 0)
                self.changeStateTo('re_calibrate')
            if not self.timer.is_waiting():
                self.currentAngle += 0.3
                print self.currentAngle
                self.timer.wait(3)
                if self.currentAngle >= 90*math.pi/180:
                    self.speak("I did not found .")
                    self.changeStateTo(STATE.ERROR)
                else:
                    Neck.turn(self.currentAngle)

        elif self.state == 're_calibrate':
            if device == Devices.base and data == 'SUCCEEDED':
                self.wait(2)
                Publish.follow_init.publish(Bool(True))
                self.changeStateTo(STATE.FOLLOWING)

    def start(self):
        self.changeStateTo(STATE.INIT)

    def stop(self, message):
        if STATE.ABORTED in message.lower():
            self.changeStateTo(STATE.ABORTED)
        elif STATE.WAITING in message.lower():
            self.changeStateTo(STATE.WAITING)
        else:
            self.changeStateTo(STATE.ERROR)
        self.stop_robot()


if __name__ == '__main__':
    FollowPerson()