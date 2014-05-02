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
        self.object_information = read_object_info()
        self.go_closer_method = 'FORWARD'
        self.LIMIT_MANIPULATED_DISTANCE = 0.78

        self.desiredObject = "kokokrunch" #NOTE 1 = cornflakes
        self.desiredObject2 = "dutchmilk"#NOTE 2 = milk
        self.state = "init"
        rospy.loginfo('Start Final Demo State')
        rospy.spin()

    def main(self, device, data):
        if(device != Devices.color_detector):
            rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))

        if self.state == 'init':
                self.move_robot('bed')
                self.state = 'wakeMasterUp'

        elif self.state == 'wakeMasterUp':
                if(device == Devices.base and data =='SUCCEEDED'):
                        self.speak("Good Morning Master.What I can do for you?")#TODO Additional Speak date & time
                        self.state = 'choice'
        
        elif self.state == 'choice':
                if(device == Devices.voice and data in 'i need breakfast,i want breakfast , i am hungry'):#TODO add another menu
                        self.speak("Now I can cook cornflake,Which menu do you want me to cook?")
                        self.state = 'select'

        elif self.state == 'select':
                if(device == Devices.voice and (data =='cornflake' or data == 'anything' or data == 'whatever')):
                        self.speak("Do you want me to cook CORNFLAKE isn\'t it?")
                        self.wait(2)
                        self.state = 'confirmMenu'
              
        elif self.state == 'confirmMenu':
                if(device == Devices.voice and (data =='confirm' or data =='robot yes' or data =='alright')):
                        self.state = 'goToCook'
        #       elif(device == Devices.voice and (data == 'cancel' or data =='i change my mind')):
        #              self.state = 'wakeMasterUp'

        elif self.state == 'goToCook':
                Publish.speak("I will go to kitchen and make you a breakfast.")
                self.move_robot('kitchen table')
                self.wait(2)
                self.state = 'readyToCook'

        elif self.state == 'readyToCook':
                if(device == Devices.base and data =='SUCCEEDED'):#debug
                        #self.state = 'serve'
                        Publish.set_manipulator_action('prepare')
                        Publish.set_height(1.1)
                        Publish.set_neck(0,-0.7,0)
                        self.state = 'setRobotEnvironment' #NOTE DEBUG

        elif self.state == 'setRobotEnvironment':
                if(device == Devices.manipulator and data == 'finish'):
                    Publish.find_object( 0.75 )
                    Publish.speak("Finding ingrediants.")
                    self.state = 'searchingCornflake'

#        elif self.state == 'searchingCornflake':
#           if device == Devices.recognition:
#                self.speak("Searching cornflake.")
#                objects = data.objects
#                for obj in objects:
#                    if obj.category == self.desiredObject:
#                        centroidVector = Vector3()
#                        centroidVector.x = obj.point.x
#                        centroidVector.y = obj.point.y
#                        centroidVector.z = obj.point.z
#                        Publish.set_manipulator_action_grasp(centroidVector)
#                        self.state = 'graspingCornflake'
        elif(self.state == 'searchingCornflake'):
            if(device == devices.recognition):
                objects = []
                print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if obj.ismanipulable == true and obj.category != "unknown" and obj.categort == self.desiredObject:
                        self.speak(obj.category)
                        centroidvector = vector3()
                        centroidvector.x = obj.point.x
                        centroidvector.y = obj.point.y
                        centroidvector.z = obj.point.z
                        self.carried_object = obj.category
                        publish.set_manipulator_action_grasp(centroidvector)
                        self.state = 'graspingcornflake'
                        return none

                for obj in objects:
                    if obj.ismanipulable == false and obj.category != "unknown":
                        self.speak("i will go closer to " + obj.category)
                        if self.go_closer_method == 'forward':
                            move_distance = obj.point.x - self.limit_manipulated_distance + 0.3
                            print '----------------------------------',move_distance
                            publish.move_relative(move_distance, 0, 0)
                            self.wait(2)
                            self.speak("i will go forward to " + obj.category)
                            self.go_closer_method = 'rotate'
                            self.state = "step_to_object"
                        elif self.go_closer_method == 'rotate':
                            rotation = math.tan(obj.point.y/obj.point.x)
                            publish.move_relative(0 ,0 ,rotation)
                            self.wait(2)
                            self.speak("i will rotate to " + obj.category)
                            self.go_closer_method = 'finish'
                            self.state = "step_to_object"
                        elif self.go_closer_method == 'finish':
                            self.index+=1
                            self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                            self.go_closer_method = 'forward'
                            self.wait(2)
                        return none

        elif(self.state == 'STEP_TO_OBJECT'):
            if(device == Devices.base and (data == 'SUCCEEDED' or data == 'ABORTED')):
                Publish.find_object(0.7)
                self.state = 'searchingCornflake'

        elif self.state == 'graspingCornflake':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'trackingBowl'

        elif self.state == 'trackingBowl':
            self.speak("Try to find a bowl")
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'discardCornflake'

        elif self.state == 'discardCornflake':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("discard cornflake.")
                self.wait(3)
                Publish.set_manipulator_action('cornflake_pullback')
                self.state = 'discarding'

        elif self.state =='discarding':
            if device == Devices.manipulator and data == 'finish':
                    Publish.find_object( 0.75 )
                    self.state = 'searchingMilk'

#        elif self.state == 'searchingMilk':
#                if device == Devices.recognition:
#                    Publish.speak("Searching milk")
#                    objects = data.objects
#                    for obj in objects:
#                        if obj.category == self.desiredObject2:
#                            centroidVector = Vector3()
#                            centroidVector.x = obj.point.x
#                            centroidVector.y = obj.point.y
#                            centroidVector.z = obj.point.z
#                            Publish.set_manipulator_action_grasp(centroidVector)
#                            self.state = 'graspingMilk'
       
	elif(self.state == 'searchingMilk'):
            if(device == devices.recognition):
                objects = []
                print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if obj.ismanipulable == true and obj.category != "unknown" and obj.categort == self.desiredObject2:
                        self.speak(obj.category)
                        centroidvector = vector3()
                        centroidvector.x = obj.point.x
                        centroidvector.y = obj.point.y
                        centroidvector.z = obj.point.z
                        self.carried_object = obj.category
                        publish.set_manipulator_action_grasp(centroidvector)
                        self.state = 'graspingcornflake'
                        return none

                for obj in objects:
                    if obj.ismanipulable == false and obj.category != "unknown":
                        self.speak("i will go closer to " + obj.category)
                        if self.go_closer_method == 'forward':
                            move_distance = obj.point.x - self.limit_manipulated_distance + 0.3
                            print '----------------------------------',move_distance
                            publish.move_relative(move_distance, 0, 0)
                            self.wait(2)
                            self.speak("i will go forward to " + obj.category)
                            self.go_closer_method = 'rotate'
                            self.state = "step_to_object"
                        elif self.go_closer_method == 'rotate':
                            rotation = math.tan(obj.point.y/obj.point.x)
                            publish.move_relative(0 ,0 ,rotation)
                            self.wait(2)
                            self.speak("i will rotate to " + obj.category)
                            self.go_closer_method = 'finish'
                            self.state = "step_to_object"
                        elif self.go_closer_method == 'finish':
                            self.index+=1
                            self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                            self.go_closer_method = 'forward'
                            self.wait(2)
                        return none

        elif(self.state == 'STEP_TO_OBJECT_2'):
            if(device == Devices.base and (data == 'SUCCEEDED' or data == 'ABORTED')):
                Publish.find_object(0.7)
		self.state = 'searchingMilk'

        elif self.state == 'graspingMilk':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'trackingBowl_2'

        elif self.state == 'trackingBowl_2':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'discardMilk'

        elif self.state == 'discardMilk':
            if device == Devices.manipulator and data == 'finish':
                self.wait(3)
		self.speak("discard milk")
                Publish.set_manipulator_action('cornflake_pullback')
                self.state = 'serve'

        elif self.state == 'serve':
             if device == Devices.manipulator and data == 'finish': #NOTE DEBUG
             #if device == Devices.base and base == 'SUCCEEDED': #NOTE DEBUG
                self.state = 'goToAlert'

        elif self.state == 'goToAlert':
                self.move_robot('bed')
                self.wait(2)
                #self.speak("walking g g g ")
                self.state = 'alert'

        elif self.state == 'alert':
                if(device == Devices.base and data == 'SUCCEEDED'):
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
