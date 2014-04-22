#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from math import pi

roslib.load_manifest('main_state')

class Cleanup_jp(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.search_seqeunce = []
        readLocationSequence(self.search_seqeunce)
        self.object_list = {}
        read_object(self.object_list)
        self.current = 0

        rospy.loginfo('Start Cleanup_jp State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:"+self.state+" from:"+device+" "+data)

        if(self.state == 'init'):
            if(device == Devices.door and data == 'open'):
                Publish.move_relative(1.5, 0)
                self.state = 'passDoor'
                Publish.set_manipulator_action('walking')

        elif(self.state == 'passDoor'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 'gotoCommand'
                self.move_robot('command_pos')

        elif(self.state == 'gotoCommand'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 'waitForCommand'

        elif(self.state == 'waitForCommand'):
            if(device == Devices.voice and 'living room' in data):
                Publish.speak('go to living room')
                # go to next pos
                self.state = 'gotoObject'
                self.move_robot(self.search_seqeunce[self.current])

        elif(self.state == 'gotoObject'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                rospy.loginfo("current pos : " + self.search_seqeunce[self.current])
                Publish.speak('wait for search')
                self.state = 'waitForSearch'

        elif(self.state == 'waitForSearch'):
            ### searching
            if(device == 'object' and data == 'found'):
                ### get object (manipulator)
                self.state = 'getObject'
            elif(device == 'object' and data == 'not found'):
                self.current += 1
                if(self.current < len(self.search_sequence)):
                    # go to next pos
                    self.state = 'gotoObject'
                    self.move_robot(self.search_seqeunce[self.current])
                else :
                    self.state = 'get_out'
                    self.move_robot('out_pos')

        elif(self.state == 'getObject'):
            if(device == Devices.manipulator and data == 'finish'):
                Publish.speak('go to place')
                self.state = 'gotoPlace'
                self.move_robot(self.search_seqeunce[self.object_list[''].place]) ####
            if(device == Devices.manipulator and data == 'error'):
                self.current += 1
                # go to next pos
                self.state = 'gotoObject'
                self.move_robot(self.search_seqeunce[self.current])

        elif(self.state == 'gotoPlace'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                ### drop object (manipulator)
                self.state = 'left'

        elif(self.state == 'left'):
            if(device == Devices.manipulator and data == 'finish'):
                # go to next pos
                self.state = 'gotoObject'
                self.move_robot(self.search_seqeunce[self.current])

        elif(self.state == 'get_out'):
            if(device == Devices.base and data == 'SUCCEEDED'):
                self.state = 'finish'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        Cleanup_jp()
    except Exception, error:
        print str(error)
