#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from geometry_msgs.msg import Vector3
from time import gmtime, strftime

roslib.load_manifest('main_state')
class FINALDEMO(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.LIMIT_MANIPULATED_DISTANCE =   0.78
        self.COOK_TABLE_HEIGTH          =   0.7
        self.ROBOT_HEIGHT               =   1.1
        self.desiredObject              =   ["kokokrunch","dutchmilk"]
        self.state                      =   "INIT"

        rospy.loginfo('Start Final Demo State')
        rospy.spin()

    def main(self, device, data):
        if device != Devices.color_detector:
            rospy.loginfo("State : " + self.state + " From : " + device + " Data : " + str(data))

        if self.state == 'INIT':
            if device == Devices.voice and 'lumyai listen'or'robot listen' in data:
                self.speak(strftime("%H O'clock %M minute.", gmtime()))
                self.speak("Good morning master.Can I help you Master?")
                self.state = 'LISTEN'
                self.wait(2)

        elif self.state == 'LISTEN':
            if device == Devices.voice and 'robot yes' in data :
                self.speak("What can I do for you?")
                self.state = 'COMMAND'
                self.wait(2)
        #TODO plan to improve
        elif self.state == 'COMMAND':
            if device == Devices.voice and 'prepare'and'breakfast' in data:
                self.speak("Do you want me to prepare a cornflake yes or no?")
                self.state = 'CONFIRM'
                self.wait(2)

        elif self.state == 'CONFIRM':
            if device == Devices.voice and 'robot yes' in data :
                self.speak("Alright, I will prepare your breakfast.")
                self.wait(2)
                self.state = 'PREPARE_FOR_ACTION'

        elif self.state == 'PREPARE_FOR_ACTION':
            Publish.set_manipulator_action('prepare')
            Publish.set_height(self.ROBOT_HEIGHT)
            Publish.set_neck(0,-0.7,0)
            self.state = 'READY_FOR_ACTION'

        elif self.state == 'READY_FOR_ACTION':
            if device == Devices.manipulator and data == 'finish':
                Publish.find_object(self.COOK_TABLE_HEIGTH)
                Publish.speak("Searching breakfast ingredients.")
                self.state = 'SEARCHING_CORNFLAKE'

        elif(self.state == 'SEARCHING_CORNFLAKE'):
            if(device == Devices.recognition):
                objects = []
                print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if obj.category == self.desiredObject[1]:
                        self.speak(obj.category)
                        centroidVector = Vector3()
                        centroidVector.x = obj.point.x
                        centroidVector.y = obj.point.y
                        centroidVector.z = obj.point.z
                        Publish.set_manipulator_action_grasp(centroidVector)
                        self.state = 'GRASPING_CORNFLAKE'
                        return None

        elif self.state == 'GRASPING_CORNFLAKE':
            if device == Devices.manipulator and data == 'finish':
                self.speak("I got it.")
                self.state = 'SEARCH_BOWL'

        elif self.state == 'SEARCHING_BOWL':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'DISCARD_CORNFLAKE'

        elif self.state == 'DISCARD_CORNFLAKE':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("discard cornflake.")
                self.wait(3)
                Publish.set_manipulator_action('cornflake_pullback')
                self.state = 'DISCARDING'

        elif self.state == 'DISCARDING':
            if device == Devices.manipulator and data == 'finish':
                Publish.find_object(self.COOK_TABLE_HEIGTH)
                self.state = 'SEARCHING_MILK'

        elif self.state == 'SEARCHING_MILK':
            if device == Devices.recognition:
                objects = []
                print '--------len(data.objects) : ' +str(len(data.objects)) + '-------'
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if obj.category == self.desiredObject[2]:
                        self.speak(obj.category)
                        centroidVector = Vector3()
                        centroidVector.x = obj.point.x
                        centroidVector.y = obj.point.y
                        centroidVector.z = obj.point.z
                        Publish.set_manipulator_action_grasp(centroidVector)
                        self.state = 'GRASPING_MILK'
                        return None

        elif self.state == 'GRASPING_MILK':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'SEARCHING_BOWL_2'

        elif self.state == 'SEARCHING_BOWL_2':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'DISCARD_MILK'

        elif self.state == 'DISCARD_MILK':
            if device == Devices.manipulator and data == 'finish':
                self.wait(3)
                Publish.set_manipulator_action('cornflake_pullback')
                self.state = 'DISCARDING_2'

        elif self.state == 'DISCARDING_2':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'GO_TO_WAKE_MASTER_UP'

        elif self.state == 'GO_TO_WAKE_MASTER_UP':
            if device == Devices.manipulator and data == 'finish':
                self.move_robot('bed')
                self.state = 'ALERT'
                self.wait(2)

        elif self.state == 'GO_TO_WAKE_MASTER_UP':
            if device == Devices.base and data == 'SUCCEEDED':
                Publish.speak("Please wake up master.")
                self.speak(strftime("%H O'clock %M minute.", gmtime()))
                #Now is . . .
                self.state = 'WAIT_FOR_ANSWER'

        elif self.state == 'WAIT_FOR_ANSWER':
            if device == Devices.voice and 'get out,i know' in data:
                self.state = 'GET_OUT'

        elif self.state == 'GET_OUT':
            self.move_robot('kitchen')
            self.state = 'FINISH'

        elif self.state == 'FINISH':
            pass

if __name__ == '__main__':
    global category
    try:
        rospy.init_node('main_state')
        FINALDEMO()
    except rospy.ROSInternalException:
        print
        str(error)
