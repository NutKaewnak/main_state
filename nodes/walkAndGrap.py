#!/usr/bin/env python
import rospy
import roslib
import math
from include.function import *
from include.publish import *
from include.base_state import *

roslib.load_manifest('main_state')

class WalkAndGrap(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.state = 'INIT'
        self.table_pos = ["hallway table"]
        self.plain_height = [1.10]
        self.intermediate_pos = "bar"
        self.index = 0
        self.max_index = 2
        self.LIMIT_MANIPULATED_DISTANCE = 0.78
        self.go_closer_method = 'FORWARD'
        rospy.loginfo('Start Cleanup_jp State')
        rospy.spin()

    def pre_manipulation(self,height):
        self.speak('initialize action')
        Publish.set_height(height)
        Publish.set_manipulator_action('prepare')
        Publish.set_neck(0,-0.70,0)

    def main(self, device, data):
        rospy.loginfo("state:"+self.state+" from:"+device+" "+str(data))

        if(self.state == 'INIT'):
            if(device == Devices.door and data == 'open'):
                Publish.move_relative(1.0, 0, 0)
                Publish.set_manipulator_action('walking')
                self.state = 'PASS_DOOR'

        elif(self.state == 'PASS_DOOR'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.move_robot(self.table_pos[self.index])
                self.wait(2)
                self.speak('go to ' + self.table_pos[self.index])
                self.state = 'GO_TO_TABLE'

        elif(self.state == 'GO_TO_TABLE'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.pre_manipulation(self.plain_height[self.index])
                self.state = 'SEARCH_OBJECT'

        elif(self.state == 'SEARCH_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                Publish.find_object(0.7)
                self.state = 'GET_SEARCHING_RESULT'

        elif(self.state == 'GET_SEARCHING_RESULT'):
            if(device == Devices.recognition):
                objects = []
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if obj.isManipulable == True and obj.category != "unknown":
                        self.speak('I will graps ' + obj.category)
                        centroidVector = Vector3()
                        centroidVector.x = obj.point.x
                        centroidVector.y = obj.point.y
                        centroidVector.z = obj.point.z
                        #Publish.set_manipulator_point(centroidVector.x,centroidVector.y,centroidVector.z)
                        self.go_closer_method = 'FORWARD'
                        #self.state = 'GET_OBJECT'
                        self.move_robot(self.intermediate_pos)
                        self.state = 'GO_TO_INTERMEDIATE_POS'
                        self.index = 0
                        return None

                for obj in objects:
                    if obj.isManipulable == False and obj.category != "unknown":
                        #self.speak("I will go closer to " + obj.category)
                        if self.go_closer_method == 'FORWARD':
                            move_distance = obj.point.x - self.LIMIT_MANIPULATED_DISTANCE + 0.3
                            print '----------------------------------',move_distance
                            #move_distance = 0.40
                            Publish.move_relative(move_distance, 0, 0)
                            self.wait(2)
                            self.speak("I will go forward to " + obj.category)
                            self.go_closer_method = 'ROTATE'
                            self.state = "STEP_TO_OBJECT"
                            #self.state = 'GO_TO_TABLE'
                        elif self.go_closer_method == 'ROTATE':
                            rotation = math.tan(obj.point.y/obj.point.x)
                            Publish.move_relative(0 ,0 ,rotation)
                            self.wait(2)
                            self.speak("I will rotate to " + obj.category)
                            self.go_closer_method = 'FINISH'
                            self.state = "STEP_TO_OBJECT"
                            #self.state = 'GO_TO_TABLE'
                        elif self.go_closer_method == 'FINISH':
                            self.move_robot(self.table_pos[self.index])
                            self.go_closer_method = 'FORWARD'
                            self.wait(2)
                            self.speak(obj.category + ' is unreachable, I will  go to ' + self.table_pos[self.index])
                            self.state = 'GO_TO_INTERMEDIATE_POS'
                        return None
                #use this to go to base location back and forth
                #self.index+=1
                if self.index < self.max_index:
                    self.move_robot(self.table_pos[self.index])
                    self.wait(2)
                    self.speak('see nothing, and go to ' + self.table_pos[self.index])
                    self.state = 'GO_TO_TABLE'
                else:
                    self.index = 0
                    self.move_robot(self.intermediate_pos)
                    self.wait(2)
                    self.speak('see nothing, and go to ' + self.intermediate_pos)
                    self.state = 'GO_TO_INTERMEDIATE_POS'

        elif(self.state == 'STEP_TO_OBJECT'):
            if(device == Devices.base and (data == 'SUCCEEDED' or data == 'ABORTED')):
                Publish.find_object(0.7)
                self.state = 'GET_SEARCHING_RESULT'

        elif(self.state == 'GET_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                self.speak('I got it, and go to ' + self.intermediate_pos)
                self.wait(2)
                self.move_robot(self.intermediate_pos)
                self.state = 'GO_TO_INTERMEDIATE_POS'

        elif(self.state == 'GO_TO_INTERMEDIATE_POS'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                #Publish.set_manipulator_action('walking')
                self.move_robot(self.table_pos[self.index])
                self.wait(2)
                self.speak('I go to ' + self.table_pos[self.index])
                self.state = 'GO_TO_TABLE'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        WalkAndGrap()
    except Exception, error:
        print str(error)
