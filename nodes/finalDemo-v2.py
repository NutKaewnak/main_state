#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from geometry_msgs.msg import Vector3
from math import pi

roslib.load_manifest('main_state')

class FINALDEMO(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.desiredObject = 1 #NOTE 1 = cornflakes
        self.desiredObject2 = 2#NOTE 2 = milk
     #       Publish.set_height(1.27)
        rospy.loginfo('Start Final Demo State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))

        if self.state == 'init':
                self.move_robot('bed')
                self.state = 'wakeMasterUp'

        elif self.state == 'wakeMasterUp':
                if(device == Devices.base and data =='SUCCEEDED'):
                        Publish.speak("Good Morning Master.What I can do for you?")#TODO Additional Speak date & time
                        self.state = 'choice'
        
        elif self.state == 'choice':
                if(device == Devices.voice and data in 'need breakfast, want breakfast , i am hungry'):#TODO add another menu
                        Publish.speak("Now I can cook cornflake,Which menu do you want me to cook?")
                        self.state = 'select'

        elif self.state == 'select':
                if(device == Devices.voice and (data =='cornflake' or data == 'anything' or data == 'whatever')):
                        Publish.speak("Do you want me to cook CORNFLAKE isn\'t it?")
                        self.wait(2)
                        self.state = 'confirmMenu'
              
        elif self.state == 'confirmMenu':
                if(device == Devices.voice and (data =='confirm' or data =='yes' or data =='alright')):
                        self.state = 'goToCook'
        #       elif(device == Devices.voice and (data == 'cancel' or data =='i change my mind')):
        #              self.state = 'wakeMasterUp'

        elif self.state == 'goToCook':
                Publish.speak("I will go kitchen and make you a breakfast.")
                self.move_robot('kitchen table')
                self.wait(2)
                self.state = 'readyToCook'

        elif self.state == 'readyToCook':
                if(device == Devices.base and data =='SUCCEEDED'):
                        Publish.find_object(String("start"))
                        Publish.speak("Finding ingrediants.")
                        self.state = 'serve'
                        #self.state = 'searchingCornflake' #NOTE DEBUG
        
        elif self.state == 'searchingCornflake':
            if device == Devices.recognition:
                Publish.speak("Searching cornflake.")
                object = []
                if data.isMove:
                    pass
                else:
                    objects = data.objects
                    for obj in objects:
                        if obj.category == self.desiredObject: 
                            centroidVector = Vector3()
                            centroidVector.x = obj.point.x
                            centroidVector.y = obj.point.y
                            centroidVector.z = obj.point.z
                            Publish.set_manipulate_grasp(centroidVector)
                            self.state = 'graspingCornflake'

        elif self.state == 'graspingCornflake':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'trackingBowl'

        elif self.state == 'trackingBowl':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'discardCornflake'

        elif self.state == 'discardCornflake':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("discard cornflake.")
                self.wait(3)
                Publish.set_manipulator_action('normal_pullback')
                if device == Devices.manipulator and data == 'finish':
                        Publish.findObject(String("start"))
                        self.state = 'searchingMilk'

        elif self.state == 'searchingMilk':
                if device == Devices.recognition:
                    Publish.speak("Searching milk")
                    object = []
                    if data.isMove:
                        pass
                    else:
                        objects = data.objects
                        for obj in objects:
                            if obj.category == desiredObject2:
                                centroidVector = Vector3()
                                centroidVector.x = obj.point.x
                                centroidVector.y = obj.point.y
                                centroidVector.z = obj.point.z
                                Publish.set_manipulator_action_grasp(centroidVector)
                                self.state = 'graspingMilk'

        elif self.state == 'graspingMilk':
            if device == Devices.manipulate and data == 'finish':
                self.state = 'trackingBowl_2'

        elif self.state == 'trackingBowl_2':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'discardMilk'

        elif self.state == 'discardMilk':
            if device == Devices.manipulate and data == 'finish':
                self.wait(3)
                Publish.set_manipulator_action('normal_pullback')
                self.state = 'serve'

        elif self.state == 'serve':
            #if device == Devices.manipulate and data == 'finish': NOTE DEBUG
             if device == Devices.base and base == 'SUCCEEDED': #NOTE DEBUG
                self.state = 'goToAlert'

        elif self.state == 'goToAlert':
                self.move_robot('bed')
                self.wait(2)
                self.state = 'alert'

        elif self.state == 'alert':
                if(device == Devices.base and data == 'SUCCEEDDED'):
                        Publish.speak("the breakfast is ready to serve.")
                        self.state = 'finish'

        elif self.state == 'finish':
            pass

if __name__ == '__main__':
    global category, send_object_point, pickObjectPublisher
    try:
        rospy.init_node('main_state')
        FINALDEMO()
    except rospy.ROSInternalException:
        print
        str(error)
