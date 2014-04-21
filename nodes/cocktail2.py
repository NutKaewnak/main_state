#!/usr/bin/env python
import rospy
import roslib
import math
from include.function import *
from include.publish import *
from include.base_state import *
#from math import pi

from object_perception.msg import Object
from object_perception.msg import ObjectContainer

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

        self.people_name = ['richard','rishard','richart','philip' ,'emma' ,'danial' ,'tina','steve' ,'henry' ,'peter','peeter' ,'robert' ,'sarah' ,'brian' ,'thomas','britney' ,'justin','tony' ,'kevin' ,'joseph','michael' ,'michelle' ,'donna']


        self.publish = Publish()
        self.object_list = ['pringles','lay','water','orange juice','green tea','milk','s','fanta','corn flakes','corn']
        #self.publish.set_height(1.27)
        self.isInit  = False
        self.currentAngle = -90*math.pi/180
        self.temp = ''
        self.currentObjectNumber = 0
        self.currentTime = 0
        #self.state = 'init'
        self.state = 'getCommand'
        self.peopleName = ''
        self.desiredObject = ''


        rospy.loginfo('Cocktail state starts.')
        rospy.spin()

    def cb_detectedObject(self, data):
        self.main('recognition',data)

    def cb_gesture(self,data):
        print 'in cb_gesture cb'
        #call(["aplay","/home/skuba/skuba_athome/main_state/sound/accept.wav"])
    #    print "delay.isWait() = " + str(delay.isWait())
    #    print "GESTURE at %f,%f,%f" % (data.point.x,data.point.y,data.point.z)
        #main_state('gesture',"%f,%f,%f" % (data.point.x,data.point.y,data.point.z))
        self.main('gesture',"%f,%f,%f" % (data.point.x,data.point.y,data.point.z))

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if(self.delay.isWait()): return None

        if self.state == 'init':
            if device == Devices.door and data == 'open':
                # move pass door
                #self.publish.pan_tilt_command(getQuaternion(0,50*math.pi/180,0))
                #self.publish.base.publish(NavGoalMsg('clear','relative',Pose2D(1.5,0,0)))
                Publish.move_relative(1.5, 0)
                self.delay.delay(1)
                self.state = 'passDoor'
            if(not self.isInit):
                #normalInitialize()
                self.publish.manipulator_action.publish(String('walking'))
                Publish.set_manipulator_action('walking')
                self.isInit = True

        elif self.state == 'passDoor':
            if device == Devices.base and data == 'SUCCEEDED':
                # send to base
                self.move_robot('kitchen')
                #self.publish.base.publish(location_list['kitchen_room'])
                self.delay.delay(3)
                self.state = 'gotoKitchenRoom'

        elif self.state == 'gotoKitchenRoom':
            if(device == Devices.base and data == 'SUCCEEDED'):
                #self.publish.pan_tilt_command(getQuaternion(0,0,self.currentAngle))

                Publish.speak("Please wave your hand.")
                #call(['espeak','Please wave your hand.','-ven+f4','-s 150'])
                self.delay.waiting(7)
                #delay.delay(3)
                self.state = 'searchGesture'
                #call(['espeak','change state to search gesture.','-ven+f4','-s 150'])


        elif self.state == 'searchGesture':
            print 'device : ' + device + ', data : ' + data
            if(device == 'gesture'):
                Publish.speak("I see you.")
                #call(['espeak','I see you.','-ven+f4','-s 150'])
                # x,y = from gesture
                x,y,z = data.split(',')
                #print 'Kinect angle : ' + str(self.currentAngle)
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                Publish.move_relative(float(x),float(y))
                #self.publish.base.publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),self.currentAngle)))
                #self.publish.pan_tilt_command(getQuaternion(0,50*math.pi/180,0))
                self.delay.delay(1)
                self.state = 'getCommand'
            if(self.delay.isWaitFinish()):
                self.currentAngle += 0.3
                #self.publish.pan_tilt_command(getQuaternion(0,0,self.currentAngle))
                self.delay.waiting(7)
                if(self.currentAngle >= 90*math.pi/180):
                    #self.publish.pan_tilt_command(getQuaternion(0,50*math.pi/180,0))
                    selfdelay.delay(1)
                    Publish.speak("I did not found anyone.")
                    #call(['espeak','I did not found anyone.','-ven+f4','-s 150'])
                    #self.publish.base.publish(location_list['bar'])			
                    self.state = 'error'

        elif self.state == 'getCommand':
            if device == Devices.base and data == 'SUCCEEDED' :
                #self.publish.pan_tilt_command(getQuaternion(0,0,0))
                self.delay.delay(1)
                Publish.speak("Hello, What is your name.")
                #call(['espeak','Hello, What is your name.','-ven+f4','-s 150'])
                self.state = 'waitForName'
    


        elif self.state == 'waitForName':
            if device == Devices.voice:
                for i in self.people_name:
                    if(i in data):
                        Publish.speak("Are you " + i)
                        #call(['espeak','Are you ' + i,'-ven+f4','-s 150'])
                        self.temp = i
                        self.state = 'ConfirmName'
                        break


        elif self.state == 'ConfirmName':
            if device == Devices.voice and 'yes' in data:
                self.peopleName = self.temp
                Publish.speak('Hello '+self.temp +' what do you want')
                #call(['espeak','Hello '+self.temp +' what do you want','-ven+f4','-s 150'])
                self.state = 'waitForObject'
            elif(device == Devices.voice and 'no' in data):

                Publish.speak('Hello,What is your name')
                #call(['espeak','Hello,What is your name','-ven+f4','-s 150'])
                self.state = 'waitForName'


        elif self.state == 'waitForObject':
            if device == Devices.voice:
                for i in self.object_list:
                    if(i in data):
                        Publish.speak('you want ' + i +' yes or no ')
                        #call(['espeak','you want ' + i +' yes or no ','-ven+f4','-s 150'])
                        self.objectName = i
                        self.state = 'ConfirmObject'
                        break



        elif self.state == 'ConfirmObject':
            if(device == Devices.voice and 'yes' in data):
                self.desiredObject = self.object_mapping[self.objectName]
                self.objectName = self.temp
                #self.publish.base.publish(location_list['bar_table_pos_'+str(self.currentTime)])
                self.move_robot('bar')
                self.delay.delay(1)
                #state  = "waitForLocation"
                self.state  = "MOVE_BASE"
            elif(device == 'voice' and 'no' in data):
                Publish.speak('Hello '+self.peopleName +' what do you want')
                #call(['espeak','Hello '+self.peopleName +' what do you want','-ven+f4','-s 150'])
                self.state = 'waitForObject'


        elif self.state == 'MOVE_BASE':	
            if(device == Devices.base and data == 'SUCCEEDED'):
                Publish.speak('I reach the destination.')
                #call(['espeak','I reach the destination.','-ven+f4','-s 150'])
                self.currentObjectNumber  = 0
                self.state = "GET_OBJECT"
                self.delay.delay(2)
                self.findObjectPointPublisher.publish(String("start"));

        elif self.state == 'GET_OBJECT':
            #if(device == Devices.recognition):
            if(device == "recognition"):
                objects = []
                #call(["aplay","/home/skuba/skuba_athome/main_state/sound/accept.wav"])
                if(data.isMove):
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
                        Publish.speak("go to next position.")
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
            if(device == Devices.manipulator and data == 'finish'):
                #call(["espeak","-ven+f4","I got it","-s 150"])
                Publish.speak("I got it.")
                #heightCmdPublisher.publish(Float64(1.1))
                #normalInitialize()
                #heightCmdPublisher.publish(Float64(1.21))
                #tiltKinectCmdPublisher.publish(Float64(-0.40))
                self.move_robot('living room')
                self.delay.delay(1)
                self.state = 'GO_TO_LIVING_ROOM_WITH_OBJECT'



        elif self.state == "GO_TO_LIVING_ROOM_WITH_OBJECT":
            if(device == Devices.base and data == 'SUCCEEDED'):
                #call(["espeak","-ven+f4",self.peopleName + ". please wave your hand.","-s 150"])
                Publish.speak(self.peopleName + ". please wave your hand.")
                #self.publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
                self.delay.waiting(3)
                self.state = 'SEARCH_GESTURE_WITH_OBJECT'


        elif self.state == 'SEARCH_GESTURE_WITH_OBJECT':
            if(device == 'gesture'):
                # x,y = from gesture
                x,y,z = data.split(',')
                x = float(z) * math.cos(currentAngle)
                y = float(z) * math.sin(currentAngle)
                Publish.move_relative(float(x),float(y))
                #self.publish.base.publish(NavGoalMsg('clear','relative',Pose2D(float(x),float(y),currentAngle)))
                #self.publish.pan_tilt_command(getQuaternion(0,50*math.pi/180,0))
                self.delay.delay(1)
                self.state = 'SERVE_ORDER'
            if(self.delay.isWaitFinish()):
                currentAngle += 0.3
                self.publish.pan_tilt_command(getQuaternion(0,0,currentAngle))
                self.delay.waiting(7)
                if(currentAngle >= 90*math.pi/180):
                    #self.publish.pan_tilt_command(getQuaternion(0,50*math.pi/180,0))
                    self.delay.delay(1)
                    call(["espeak","-ven+f4","lost master","-s 150"])
                    #self.publish.base.publish(location_list['bar'])			

        elif self.state == 'SERVE_ORDER':
            if(device == Devices.base and data == 'SUCCEEDED'):
                #self.publish.pan_tilt_command(getQuaternion(0,0,0))
                self.delay.delay(1)
                Publish.speak('This is your order. please take it.')
                #call(['espeak','This is your order. please take it.','-ven+f4','-s 150'])
                self.delay.delay(5)
                self.publish.manipulator_action.publish(String('walking'))
                self.delay.delay(3)
                self.move_robot('outside_pos')
                #self.publish.base.publish(location_list['out_side'])			
                self.state = 'get out'

        elif self.state == 'get out':
            if(device == Device.base and data == 'SUCCEEDED'):
                self.state = 'finish'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        CockTailParty()
    except Exception, error:
        print str(error)
