#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from include.object_information import *
from include.location_information import *
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
        self.carried_object  = ''
        self.object_information = read_object_info()
        self.go_closer_method = 'FORWARD'
        self.LIMIT_MANIPULATED_DISTANCE = 0.78

        self.table_mapping = {}
        self.table_mapping['hallway table']  = 'table_1'
        self.table_mapping['umbrella stand']  = 'table_1'
        self.table_mapping['hanger']  = 'table_2'
        self.table_mapping['bench']  = 'table_2'
        self.table_mapping['bar']  = 'table_3'
#
#        print '--------------------------'
#        print self.object_information.get_object('silicone').name
#        print self.object_information.get_object('silicone').isManipulate
        #print self.object_information.get_category('cleaning stuff')

#        self.table_mapping['6']  = 'table_3'
#        self.table_mapping['7']  = 'table_4'

        #print type(self.location_list['living room'].locations)
        #name = self.location_list['living room'].locations[0]
        #print self.location_list[self.location_list['living room'].locations[self.index]].height

#        print self.location_list['living room'].locations
#        print self.location_list['living room'].locations[0].height

        #self.object_information.get_object().category
        #object_information.get_category('food')
        #print self.object_information.get_object('pringles').location

        self.room_list = []
        for i in self.location_list:
            if isinstance(self.location_list[i],RoomInfo):
                self.room_list.append(i)

        #print self.location_list['hallway table'].height

        #print type(self.location_list['kitchen'])
        #print type(self.location_list['kitchen'].locations)
        #for i in  range(len(self.location_list['kitchen'].locations)):
        #    print self.location_list['kitchen'].locations[i]

#        self.locations={}
#        self.locations['living room'] = ['dinner table','couch table','sofa']
#        self.locations['kitchen'] = ['kitchen counter','kitchen table']
#        self.plain_height={}
#        self.plain_height['living room'] = [1.3,1.4,1.5]
#        self.plain_height['kitchen'] = [1.3,1.4]
#
#        self.proper_location = {}
#        self.proper_location['drinks'] = 'fridge'
#        self.proper_location['cleaning stuff'] = 'sink'
#        self.proper_location['food'] = 'bar'
#        self.proper_location['snacks'] = 'stove'
#        self.proper_location['unknown'] = 'trash bin'
#
#        self.picked_object = ''
#        self.category = {}
#        self.category['drinks'] = ['nescafe','minute_maid']
#        self.category['cleaning stuff'] = ['sunlight']
#        self.category['food'] = ['pringles','knorr']
#        self.category['snacks'] = ['peter_pan','redondo']

        self.cleaning_location = ''
        rospy.loginfo('Start Cleanup_jp State')
        rospy.spin()

    def pre_manipulation(self,height):
        self.speak('initialize action')
        Publish.set_height(height + 0.4)
        Publish.set_manipulator_action('prepare')
        Publish.set_neck(0,-0.70,0)


    def main(self, device, data):
        rospy.loginfo("state:"+self.state+" from:"+device+" "+str(data))

        if(self.state == 'INIT'):
            if(device == Devices.door and data == 'open'):
                Publish.set_neck(0,-0.70,0)
                Publish.move_relative(1.5, 0, 0)
                self.state = 'PASS_DOOR'
                #Publish.set_manipulator_action('walking')

        elif(self.state == 'PASS_DOOR'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                Publish.set_neck(0,-0.70,0)
                self.move_robot('bar')
                self.wait(1)
                self.state = 'WAIT_FOR_COMMAND'

        elif(self.state == 'WAIT_FOR_COMMAND'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                Publish.set_neck(0,0,0)
                self.state = 'WAIT_FOR_LOCATION'
                self.speak('Which place do you want me to clean?')

        elif(self.state == 'WAIT_FOR_LOCATION'):
            if(device == Devices.voice and data in self.room_list ):#'living room' in data):
                self.cleaning_location = data
                self.speak(data + ', yes or no?')
                self.state = 'CONFIRM_LOCATION'

        elif(self.state == 'CONFIRM_LOCATION'):
            if(device == Devices.voice and 'yes' in data):
                self.speak('I will go to ' + self.location_list[self.cleaning_location].locations[self.index])
                # go to next pos
                self.number_of_position = len(self.location_list[self.cleaning_location].locations)
                Publish.set_neck(0,-0.70,0)
                self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                self.wait(1)
                print self.location_list[self.cleaning_location].locations
                self.state = 'GO_TO_OBJECT_LOCATION'
            elif (device == Devices.voice and 'no' in data):
                self.speak('Which place do you want me to clean?')
                self.state = "WAIT_FOR_LOCATION"

        elif(self.state == 'GO_TO_OBJECT_LOCATION'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                #self.pre_manipulation(self.plain_height[self.cleaning_location][self.index])
                self.pre_manipulation(self.location_list[self.cleaning_location].height)
                self.state = 'SEARCH_OBJECT'

        elif(self.state == 'SEARCH_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                Publish.find_object(self.location_list[self.location_list[self.cleaning_location].locations[self.index]].height)
                self.state = 'GET_SEARCHING_RESULT'

        elif(self.state == 'GET_SEARCHING_RESULT'):
            if(device == Devices.recognition):
                objects = []
                #call(["aplay","/home/skuba/skuba_athome/main_state/sound/accept.wav"])
                print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'

                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    #if obj.category != "unknown":
                    if obj.isManipulable == True and obj.category != "unknown" and self.object_information.get_object(obj.category).isManipulate:
                        self.speak("I will grasp " + obj.category)
                        centroidVector = Vector3()
                        centroidVector.x = obj.point.x
                        centroidVector.y = obj.point.y
                        centroidVector.z = obj.point.z
                        #self.publish.manipulator_point.publish(centroidVector)
                        #return None
                        #Publish.set_manipulator_point(centroidVector)
                        #print obj.category,str(self.category)
                        #self.carried_object_type = self.object_information.get_object(obj.category).category
                        self.carried_object = obj.category
                        #print self.carried_object_type
                        Publish.set_manipulator_point(centroidVector.x,centroidVector.y,centroidVector.z)
                        self.state = 'GET_OBJECT'
                        self.go_closer_method = 'FORWARD'
                        return None

                for obj in objects:
                    if obj.isManipulable == False and obj.category != "unknown" and self.object_information.get_object(obj.category).isManipulate:
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
                        elif self.go_closer_method == 'ROTATE':
                            rotation = math.tan(obj.point.y/obj.point.x)
                            Publish.move_relative(0 ,0 ,rotation)
                            self.wait(2)
                            self.speak("I will rotate to " + obj.category)
                            self.go_closer_method = 'FINISH'
                            self.state = "STEP_TO_OBJECT"
                        elif self.go_closer_method == 'FINISH':
                            self.index+=1
                            if(self.table_mapping[self.location_list[self.cleaning_location].locations[self.index]] == self.table_mapping[self.location_list[self.cleaning_location].locations[self.index-1]]):
                                Publish.move_relative(-1.0, 0, 0)
                                self.wait(1)
                                #self.speak(obj.category + ' is unreachable, I will  go to ' + self.location_list[self.cleaning_location].locations[self.index])
                                self.speak("I see nothing, I am moving back.")
                                self.state = 'MOVE_BACK'
                            else:
                                self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                                self.wait(1)
                                self.speak(obj.category + ' is unreachable, I will  go to ' + self.location_list[self.cleaning_location].locations[self.index])
                                print 'self.index',self.index,'self.number_of_position',self.number_of_position
                                self.state = 'GO_TO_OBJECT_LOCATION'
 
                            #self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                            self.go_closer_method = 'FORWARD'
                            #self.wait(2)
                            #self.speak(obj.category + ' is unreachable, I will  go to ' + self.location_list[self.cleaning_location].locations[self.index])
                            #self.state = 'GO_TO_OBJECT_LOCATION'
                        return None

                if self.index < self.number_of_position:
                    #self.location_list[self.cleaning_location].locations[self.index]
                    #self.move_robot(self.locations[self.cleaning_location][self.index])
                    self.index+=1
                else:
                    self.index = 0

                if(self.table_mapping[self.location_list[self.cleaning_location].locations[self.index]] == self.table_mapping[self.location_list[self.cleaning_location].locations[self.index-1]]):
                    Publish.move_relative(-1.0, 0, 0)
                    self.speak("I see nothing, I am moving back.")
                    #self.speak('I see nothing. I will go to ' + self.location_list[self.cleaning_location].locations[self.index])
                    self.wait(1)
                    self.state = 'MOVE_BACK'
                else:
                    self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                    self.speak('I see nothing. I will go to ' + self.location_list[self.cleaning_location].locations[self.index])
                    self.wait(1)
                    print 'self.index',self.index,'self.number_of_position',self.number_of_position
                    self.state = 'GO_TO_OBJECT_LOCATION'

        elif(self.state == 'MOVE_BACK'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                self.speak('I will go to ' + self.location_list[self.cleaning_location].locations[self.index])
                self.wait(1)
                print 'self.index',self.index,'self.number_of_position',self.number_of_position
                self.state = 'GO_TO_OBJECT_LOCATION'

        elif(self.state == 'STEP_TO_OBJECT'):
            if(device == Devices.base and (data == 'SUCCEEDED' or data == 'ABORTED')):
                Publish.find_object(self.location_list[self.location_list[self.cleaning_location].locations[self.index]].height)
                self.state = 'GET_SEARCHING_RESULT'

        elif(self.state == 'GET_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
        #print self.object_information.get_object('pringles').location
                self.speak('I will go to ' + self.object_information.get_object(self.carried_object).location)
                self.move_robot(self.object_information.get_object(self.carried_object).location)
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
                self.speak("I am at " + self.object_information.get_object(self.carried_object).location)
                #self.state = 'PLACE_OBJECT'
                #PLACE OBJECT ACTION
                #Publish.set_manipulator_action('place_object')
                Publish.set_manipulator_action('normal')
                self.state = 'WAIT_FOR_HELP'
#                self.wait(1)
#                self.speak('Please bring ' + self.carried_object + ' to ' + self.object_information.get_object(self.carried_object).location)
#                self.wait(5)
#                Publish.set_manipulator_action('grip_open')
#                self.wait(3)
#
#                if self.index < self.number_of_position:
#                    self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
#                    self.speak("I am moving to " + self.location_list[self.cleaning_location].locations[self.index])
#                    self.wait(1)
#                    #self.index+=1
#                    print 'self.index',self.index,'self.number_of_position',self.number_of_position
#                    self.state = 'GO_TO_OBJECT_LOCATION'
#                else:
#                    self.state = 'GET_OUT'
#                    self.speak("I finish cleaning.")
#                    pass


        elif(self.state == 'WAIT_FOR_HELP'):
            if(device == Devices.manipulator and data == 'finish'):
                self.speak('Please bring ' + self.carried_object + ' to ' + self.object_information.get_object(self.carried_object).location)
                self.wait(10)
                self.state = "WAIT_FOR_PICKING"

        elif(self.state == "WAIT_FOR_PICKING"):
            Publish.set_manipulator_action('grip_open')

            # go to next pos
            if self.index < self.number_of_position:
                self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                self.speak("I am moving to " + self.location_list[self.cleaning_location].locations[self.index])
                self.wait(1)
                #self.index+=1
                print 'self.index',self.index,'self.number_of_position',self.number_of_position
                self.state = 'GO_TO_OBJECT_LOCATION'
            else:
                self.state = 'GET_OUT'
                self.speak("I finish cleaning.")
                pass


        elif(self.state == 'PLACE_OBJECT'):
            if(device == Devices.manipulator and data == 'finish'):
                # go to next pos
                if self.index < self.number_of_position:
                    self.move_robot(self.location_list[self.cleaning_location].locations[self.index])
                    self.speak("I am moving to " + self.location_list[self.cleaning_location].locations[self.index])
                    self.wait(1)
                    #self.index+=1
                    print 'self.index',self.index,'self.number_of_position',self.number_of_position
                    self.state = 'GO_TO_OBJECT_LOCATION'
                else:
                    self.state = 'GET_OUT'
                    self.speak("I finish cleaning.")
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
