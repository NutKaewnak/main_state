#!/usr/bin/env python
import rospy
import roslib
import math
from include.function import *
from include.publish import *
from include.base_state import *
from include.delay import *

#from object_perception.msg import Object
#from object_perception.msg import ObjectContainer

roslib.load_manifest('main_state')

class CockTailParty(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.findObjectPointPublisher = rospy.Publisher('/localization', String)

        rospy.Subscriber("/gesture/point", PointStamped, self.cb_gesture)
        rospy.Subscriber("/detected_object", ObjectContainer, self.cb_detectedObject)
        self.object_mapping = {}
        self.object_mapping['green tea'] = 1
        self.object_mapping['water'] = 2
        self.object_mapping['est'] = 3
        self.object_mapping['fanta'] = 4
        self.object_mapping['corn flakes'] = 5
        self.object_mapping['lay'] = 6
        self.object_mapping['pringles'] = 7
        self.object_mapping['milk'] = 8
        self.object_mapping['orange juice'] = 9
        self.object_mapping['milo'] = 10

        self.people_name = ['michael','christopher','matthew','joshua','daniel','david','andrew','james','justin','joseph','jessica','ashley','brittany','amanda','samantha','sarah','stephanie','jennifer','elizabeth','lauren']
        self.object_list = ['pringles','lay','water','apple juice','green tea','milk','s','fanta','corn flakes','corn']

        self.publish = Publish()
        self.isInit  = False
        self.currentAngle = -90*math.pi/180
        self.temp = ''
        self.currentObject = 0
        self.totalObject = 1
        self.currentTime = 0
        self.peopleName = []
        self.objectName = []
        self.desiredObject = ''
        #self.state = 'searchGesture'

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
                self.publish.move_relative(1.5, 0)
                self.state = 'passDoor'
            if not self.isInit:
                self.publish.set_manipulator_action('walking')
                self.isInit = True

        elif self.state == 'passDoor':
            if device == Devices.base and data == 'SUCCEEDED':
                self.move_robot('kitchen')
                self.state = 'gotoKitchenRoom'

        elif self.state == 'gotoKitchenRoom':
            if device == Devices.base and data == 'SUCCEEDED':
                self.publish.set_neck(0, 0, self.currentAngle)
                self.speak("Please wave your hand.")
                self.timer = Delay()
                self.state = 'searchGesture'

        elif self.state == 'searchGesture':
            if device == 'gesture':
                self.speak("I see you.")
                x,y,z = data.split(',') # x,y = from gesture
                #print 'Kinect angle : ' + str(self.currentAngle)
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                self.publish.move_relative(float(x),float(y))
                ###self.publish.set_neck(getQuaternion(0,50*math.pi/180,0))
                self.state = 'getCommand'
            if not self.timer.is_waiting():
                self.currentAngle += 0.3
                print self.currentAngle
                self.timer.wait(5)
                if self.currentAngle >= 90*math.pi/180:
                    self.speak("I did not found anyone.")
                    self.state = 'error'
                else:
                    self.publish.set_neck(0, 0, self.currentAngle)

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
            if device == Devices.voice and 'yes' in data:
                self.peopleName.append(self.temp)
                self.speak('Hello ' + self.temp + ', what do you want?')
                self.state = 'waitForObject'
            elif device == Devices.voice and 'no' in data:
                self.speak('Hello, What is your name?')
                self.state = 'waitForName'

        elif self.state == 'waitForObject':
            if device == Devices.voice:
                for i in self.object_list:
                    if i in data:
                        self.speak('you want ' + i +' yes or no?')
                        self.temp = i
                        self.state = 'ConfirmObject'
                        break

        elif self.state == 'ConfirmObject':
            if device == Devices.voice and 'yes' in data:
                self.objectName.append(self.temp)
                #self.desiredObject = self.object_mapping[self.temp]
                self.currentObject += 1
                if self.currentObject == self.totalObject:
                    self.currentAngle = -90*math.pi/180
                    self.currentObject  = 0
                    self.move_robot('bar')
                    self.state = "MOVE_BASE"
                else:
                    self.move_robot('kitchen')
                    self.state = "gotoKitchenRoom"
            elif device == 'voice' and 'no' in data:
                self.speak('Hello ' + self.peopleName[self.currentObject] + ' what do you want?')
                self.state = 'waitForObject'

        elif self.state == 'MOVE_BASE':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('I reach the destination.')
                self.state = "PICK_OBJECT"
                #self.state = "GET_OBJECT"
                #self.findObjectPointPublisher.publish(String("start"))

        elif self.state == 'GET_OBJECT':
            if device == "recognition":
                objects = []
                if data.isMove:
                    #go closer
                    pass
                else:
                    print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'
                    objects = data.objects
                    for obj in objects:
                        if obj.category == self.desiredObject:
                            centroidVector = Vector3()
                            centroidVector.x = obj.point.x
                            centroidVector.y = obj.point.y
                            centroidVector.z = obj.point.z

                            self.publish.manipulator_point.publish(centroidVector)
                            return None
                            #manipulateInitialize()
                            #heightCmdPublisher.publish(Float64(1.3))
                            #heightCmdPublisher.publish(Float64(1.41))
                            #delay.delay(2)

                            #publihser sending Vector3 to manipulator node to perform manipulation
                            #pickObjectPublisher.publish(centroidVector)
                            #state = "PICK_OBJECT"
                            #return None
                        print "type : " + str(obj.category) + " x : " + str(centroidVector.x) + " y : " + str(centroidVector.y) + " z : " + str(centroidVector.z)

                    if( self.currentTime < movingTime):
                        self.speak("go to next position.")
                        #call(["espeak","-ven+f4","go to next position.","-s 150"])
                        rospy.loginfo("go to next position")

                        #state = 'ERROR'
                        #self.publish.base.publish(NavGoalMsg('clear','relative',Pose2D(0,0.2,0)))

                        #self.publish.base.publish(location_list['bar_table_pos_'+str(self.currentTime)])

                        self.delay.delay(1)
                        self.currentTime += 1
                        self.state = 'MOVE_BASE'
                    else:
                        self.state = "ERROR"

        elif self.state == "PICK_OBJECT":
            if device == Devices.manipulator and data == 'finish':
                self.speak("I got it.")
                self.move_robot('living room')
                self.state = 'GO_TO_LIVING_ROOM_WITH_OBJECT'

        elif self.state == "GO_TO_LIVING_ROOM_WITH_OBJECT":
            if device == Devices.base and data == 'SUCCEEDED':
                self.publish.set_neck(0, 0, self.currentAngle)
                self.speak(self.peopleName[self.currentObject] + ". please wave your hand.")
                self.state = 'SEARCH_GESTURE_WITH_OBJECT'

        elif self.state == 'SEARCH_GESTURE_WITH_OBJECT':
            if device == 'gesture':
                self.speak("I see you.")
                x,y,z = data.split(',') # x,y = from gesture
                #print 'Kinect angle : ' + str(self.currentAngle)
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                self.publish.move_relative(float(x),float(y))
                ###self.publish.set_neck(getQuaternion(0,50*math.pi/180,0))
                self.state = 'SERVE_ORDER'
            if not self.timer.is_waiting():
                self.currentAngle += 0.3
                print self.currentAngle
                self.timer.wait(5)
                if self.currentAngle >= 90*math.pi/180:
                    self.speak("I did not found anyone.")
                    self.state = 'error'
                else:
                    self.publish.set_neck(0, 0, self.currentAngle)

        elif self.state == 'SERVE_ORDER':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('This is your order. please take it.')
                self.publish.set_manipulator_action('normal_pullback')
                self.wait(7)
                self.state = 'WAIT_FOR_SERVE'

        elif self.state == 'WAIT_FOR_SERVE':
            self.publish.set_manipulator_action('grip_open')
            self.publish.set_manipulator_action('walking')
            self.wait(2)
            self.state = 'CHECK_OBJECT'

        elif self.state == 'CHECK_OBJECT':
            if device == Devices.manipulator and data == 'finish':
                self.currentObject += 1
                if self.currentObject == self.totalObject:
                    self.move_robot('outside_pos')
                    self.state = 'get out'
                else:
                    self.move_robot('bar')
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
