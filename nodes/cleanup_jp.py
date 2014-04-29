#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
import math

roslib.load_manifest('main_state')

class Cleanup_jp(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.state = 'INIT'
        self.search_seqeunce = []
        readLocationSequence(self.search_seqeunce)
        self.object_list = {}
        read_object(self.object_list)
        self.index = 0
        self.number_of_position = 1

        self.locations={}
        self.locations['living room'] = ['dinner table','couch table','sofa']
        self.locations['kitchen'] = ['kitchen counter','kitchen table']
        self.plain_height={}
        self.plain_height['living room'] = [1.3,1.4,1.5]
        self.plain_height['kitchen'] = [1.3,1.4]

        self.proper_location = {}
        self.proper_location['drinks'] = 'fridge'
        self.proper_location['cleaning stuff'] = 'sink'
        self.proper_location['food'] = 'bar'
        self.proper_location['snacks'] = 'stove'
        self.proper_location['unknown'] = 'trash bin'

        self.picked_object = ''
        self.category = {}
        self.category['drinks'] = ['nescafe','minute_maid']
        self.category['cleaning stuff'] = ['sunlight']
        self.category['food'] = ['pringles','knorr']
        self.category['snacks'] = ['peter_pan','redondo']

        self.cleaning_location = ''


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
                Publish.move_relative(1.5, 0, 0)
                self.state = 'PASS_DOOR'
                #Publish.set_manipulator_action('walking')

        elif(self.state == 'PASS_DOOR'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.move_robot('living room')
                self.wait(1)
                self.state = 'WAIT_FOR_COMMAND'

        elif(self.state == 'WAIT_FOR_COMMAND'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 'WAIT_FOR_LOCATION'
                self.speak('Which place do you want me to clean?')

        elif(self.state == 'WAIT_FOR_LOCATION'):
            if(device == Devices.voice and data in self.locations ):#'living room' in data):
                self.cleaning_location = data
                self.speak(data + ', yes or no?')
                self.state = 'CONFIRM_LOCATION'

        elif(self.state == 'CONFIRM_LOCATION'):
            if(device == Devices.voice and 'yes' in data):
                self.speak('I will go to ' + self.cleaning_location)
                # go to next pos
                self.number_of_position = len(self.locations[self.cleaning_location])
                self.move_robot(self.locations[self.cleaning_location][self.index])
                self.wait(1)
                self.index+=1
                print 'self.index',self.index,'self.number_of_position',self.number_of_position
                self.state = 'GO_TO_OBJECT_LOCATION'
            elif (device == Devices.voice and 'no' in data):
                self.speak('Which place do you want me to clean?')
                self.state = "WAIT_FOR_LOCATION"

        elif(self.state == 'GO_TO_OBJECT_LOCATION'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.pre_manipulation(self.plain_height[self.cleaning_location][self.index-1])
                self.state = 'SEARCH_OBJECT'

        elif(self.state == 'SEARCH_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                Publish.find_object(0.7)
                self.state = 'GET_SEARCHING_RESULT'

        elif(self.state == 'GET_SEARCHING_RESULT'):
            if(device == Devices.recognition):
                objects = []
                #call(["aplay","/home/skuba/skuba_athome/main_state/sound/accept.wav"])
                if(data.isMove):
                    pass
                else:
                    print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'
                    objects = data.objects
                    for obj in objects:
                        print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                    for obj in objects:
                        #if obj.category != "unknown":
                        if obj.isManipulable == True and obj.category != "unknown":
                            self.speak(obj.category)
                            centroidVector = Vector3()
                            centroidVector.x = obj.point.x
                            centroidVector.y = obj.point.y
                            centroidVector.z = obj.point.z
                            #self.publish.manipulator_point.publish(centroidVector)
                            #return None
                            #Publish.set_manipulator_point(centroidVector)
                            print obj.category,str(self.category)
                            for cate in self.category:
                                if obj.category in self.category[cate]:
                                    self.speak('I will grasp' + obj.category)
                                    self.carried_object_type = cate
                                    self.state = 'GET_OBJECT'
                                    Publish.set_manipulator_point(centroidVector.x,centroidVector.y,centroidVector.z)
                                    return None
                    if self.index < self.number_of_position:
                        self.move_robot(self.locations[self.cleaning_location][self.index])
                        self.speak('I see nothing. I will go to ' + self.locations[self.cleaning_location][self.index])
                        self.delay(1)
                        self.index+=1
                        print 'self.index',self.index,'self.number_of_position',self.number_of_position
                        self.state = 'GO_TO_OBJECT_LOCATION'
                    else:
                        #redo a search?
                        pass

        elif(self.state == 'GET_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                self.speak('I will go to ' + self.proper_location[self.carried_object_type])
                self.move_robot(self.proper_location[self.carried_object_type])
                self.wait(1)
                self.state = 'GO_TO_PROPER_LOCATION'
#
#            if(device == Devices.manipulator and data == 'error'):
#                self.index += 1
#                # go to next pos
#                self.state = 'GO_TO_OBJECT_LOCATION'
#                self.move_robot(self.search_seqeunce[self.index])

        elif(self.state == 'GO_TO_PROPER_LOCATION'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                ### drop object (manipulator)
                self.speak("I am where it is supposed to be.")
                self.state = 'PLACE_OBJECT'
                #PLACE OBJECT ACTION
                Publish.set_manipulator_action('place')

        elif(self.state == 'PLACE_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                # go to next pos
                if self.index < self.number_of_position:
                    self.move_robot(self.locations[self.cleaning_location][self.index])
                    self.speak("I am moving to " + self.locations[self.cleaning_location][self.index])
                    self.wait(1)
                    #self.index+=1
                    print 'self.index',self.index,'self.number_of_position',self.number_of_position
                    self.state = 'GO_TO_OBJECT_LOCATION'
                else:
                    self.state = 'GET_OUT'
                    pass

        elif(self.state == 'GET_OUT'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 'finish'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        Cleanup_jp()
    except Exception, error:
        print str(error)
