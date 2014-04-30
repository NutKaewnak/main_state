#!/usr/bin/env python
import rospy
import roslib
import math
from include.function import *
from include.publish import *
from include.base_state import *
from include.delay import *
from geometry_msgs.msg import Vector3, Pose2D
from lumyai_navigation_msgs.msg import NavGoalMsg

roslib.load_manifest('main_state')

class CockTailParty(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.findObjectPointPublisher = rospy.Publisher('/localization', String)

        rospy.Subscriber("/gesture/point", PointStamped, self.cb_gesture)
        rospy.Subscriber("/detected_object", ObjectContainer, self.cb_detectedObject)

        self.people_name = ['michael','christopher','matthew','joshua','daniel','david','andrew','james','justin','joseph','jessica','ashley','brittany','amanda','samantha','sarah','stephanie','jennifer','elizabeth','lauren']

        self.isInit  = False
        self.currentAngle = -90*math.pi/180
        self.temp = ''
        self.currentObject = 0
        self.totalObject = 3
        self.peopleName = []
        self.objectName = []
        self.desiredObject = ''

        rospy.loginfo('Cocktail state starts.')
        rospy.spin()

    def cb_detectedObject(self, data):
        self.main('recognition',data)

    def cb_gesture(self,data):
        print 'in cb_gesture cb'
        self.main('gesture',"%f,%f,%f" % (data.point.x,data.point.y,data.point.z))

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if self.state == 'init':
            if device == Devices.door and data == 'open':
                Publish.move_relative(1.5, 0, 0)
                self.state = 'passDoor'
            if not self.isInit:
                Publish.set_manipulator_action('walking')
                self.isInit = True

        elif self.state == 'passDoor':
            if device == Devices.base and data == 'SUCCEEDED':
                self.move_robot('bench')
                self.state = 'gotoKitchenRoom'

        elif self.state == 'gotoKitchenRoom':
            if device == Devices.base and data == 'SUCCEEDED':
                self.currentAngle = -90*math.pi/180
                Publish.set_neck(0, 0, self.currentAngle)
                self.speak("Please wave your hand.")
                self.timer = Delay()
                self.state = 'searchGesture'

        elif self.state == 'searchGesture':
            if device == 'gesture':
                self.speak("I see you.")
                x,y,z = data.split(',')
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                Publish.move_relative(float(x),float(y), 0)
                self.state = 'getCommand'
            if not self.timer.is_waiting():
                self.currentAngle += 0.3
                print self.currentAngle
                self.timer.wait(3)
                if self.currentAngle >= 90*math.pi/180:
                    self.speak("I did not found anyone.")
                    self.state = 'error'
                else:
                    Publish.set_neck(0, 0, self.currentAngle)

        elif self.state == 'getCommand':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak("Hello, What is your name?")
                self.state = 'waitForName'

        elif self.state == 'waitForName':
            if device == Devices.voice:
                for i in self.people_name:
                    if i in data:
                        self.speak("Are you " + i + "?")
                        self.temp = i
                        self.state = 'ConfirmName'
                        break

        elif self.state == 'ConfirmName':
            if device == Devices.voice and 'robot yes' in data:
                self.peopleName.append(self.temp)
                self.speak('Hello ' + self.temp + ', what do you want?')
                self.state = 'waitForObject'
            elif device == Devices.voice and 'robot no' in data:
                self.speak('Hello, What is your name?')
                self.state = 'waitForName'

        elif self.state == 'waitForObject':
            if device == Devices.voice:
                object_found = self.object_info.get_object_from_str(data)
                if len(object_found) >= 1:
                    i = object_found[0]
                    self.speak('you want ' + i +',yes or no?')
                    self.temp = i
                    self.state = 'ConfirmObject'

        elif self.state == 'ConfirmObject':
            if device == Devices.voice and 'robot yes' in data:
                self.objectName.append(self.temp)
                self.currentObject += 1
                if self.currentObject == self.totalObject:
                    self.currentObject  = 0
                    self.speak('I go to the destination.')
                    self.move_robot('hallway table')
                    self.state = "MOVE_BASE"
                else:
                    self.speak('I go to the kitchen.')
                    self.move_robot('bench')
                    self.state = "gotoKitchenRoom"
            elif device == Devices.voice and 'robot no' in data:
                self.speak('Hello ' + self.peopleName[self.currentObject] + ' what do you want?')
                self.state = 'waitForObject'

        elif self.state == 'MOVE_BASE':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('I reach the destination.')
                Publish.set_height(1.1)
                Publish.set_manipulator_action('prepare')
                Publish.set_neck(0,-0.70,0)
                self.state = "PREPARE"

        elif self.state == 'PREPARE':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'OBJECT_SEARCH'
                Publish.find_object(0.7)

        elif self.state == 'OBJECT_SEARCH':
            if device == Devices.recognition:
                found = False
                for object in data.objects:
                    rospy.loginfo(object.category)
                    if object.category == self.objectName[self.currentObject]:
                        found = True
                        objCentroid = Vector3()
                        objCentroid.x = object.point.x
                        objCentroid.y = object.point.y
                        objCentroid.z = object.point.z
                        Publish.set_manipulator_point(objCentroid.x, objCentroid.y, objCentroid.z)
                        rospy.loginfo('%s is at x:%f y:%f z:%f'%(self.objectName[self.currentObject],objCentroid.x,objCentroid.y,objCentroid.z))
                        self.state = 'GET_OBJECT'
                        self.speak('I found %s' % self.objectName[self.currentObject])
                if not found:
                    self.neck_counter += 1
                    if self.current_action >= 90.0 * math.pi / 180.0:
                        self.speak('%s not found'%self.current_action.object)
                        #self.move_robot(self.starting_point)
                        self.wait(2)
                        #self.state = 'deliver'
                    if self.neck_counter % 2 == 0:
                        self.current_angle += 0.2
                        Publish.set_neck(0, 0, self.current_angle)
                    else:
                        Publish.set_neck(0, 0, -1.0 * self.current_angle)

        elif self.state == 'GET_OBJECT':
            if device == Devices.manipulator and data == 'finish':
                self.speak("I got it.")
                self.move_robot('bench')
                self.state = 'GO_TO_LIVING_ROOM_WITH_OBJECT'

        elif self.state == "GO_TO_LIVING_ROOM_WITH_OBJECT":
            if device == Devices.base and data == 'SUCCEEDED':
                self.currentAngle = -90*math.pi/180
                Publish.set_neck(0, 0, self.currentAngle)
                self.speak(self.peopleName[self.currentObject] + ". please wave your hand.")
                self.state = 'SEARCH_GESTURE_WITH_OBJECT'

        elif self.state == 'SEARCH_GESTURE_WITH_OBJECT':
            if device == 'gesture':
                self.speak("I see you.")
                x,y,z = data.split(',')
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                Publish.move_relative(float(x),float(y), 0)
                self.state = 'SERVE_ORDER'
            if not self.timer.is_waiting():
                self.currentAngle += 0.3
                print self.currentAngle
                self.timer.wait(5)
                if self.currentAngle >= 90*math.pi/180:
                    self.speak("I did not found anyone.")
                    self.state = 'error'
                else:
                    Publish.set_neck(0, 0, self.currentAngle)

        elif self.state == 'SERVE_ORDER':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('This is your order. please take it.')
                Publish.set_manipulator_action('normal_pullback')
                self.state = 'WAIT_FOR_SERVE'

        elif self.state == 'WAIT_FOR_SERVE':
            if device == Devices.manipulator and data == 'finish':
                self.wait(3)
                self.state = 'GRIP_OPEN'

        elif self.state == 'GRIP_OPEN':
            self.speak('gripper open.')
            Publish.set_manipulator_action('grip_open')
            self.state = 'WALKING'

        elif self.state == 'WALKING':
            if device == Devices.manipulator and data == 'finish':
                Publish.set_manipulator_action('walking')
                self.state = 'CHECK_OBJECT'

        elif self.state == 'CHECK_OBJECT':
            if device == Devices.manipulator and data == 'finish':
                self.currentObject += 1
                if self.currentObject == self.totalObject:
                    self.speak('I am leaving.')
                    self.move_robot('hallway table')
                    self.state = 'get out'
                else:
                    self.speak('I go to the destination.')
                    self.move_robot('bench')
                    self.state = "MOVE_BASE"

        elif self.state == 'get out':
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'finish'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        CockTailParty()
    except Exception, error:
        print str(error)
