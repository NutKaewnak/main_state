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
        #self.findObjectPointPublisher = rospy.Publisher('/localization', String)
        self.desiredObject = 1 #NOTE 1 = cornflakes
        self.desiredObject2 = 2#NOTE 2 = milk
        Publish.set_height(1.27)
        #rospy.Subscriber("/detected_object", ObjectContainer, self.cb_detectedObject)
        rospy.loginfo('Start Final Demo State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))

        if self.state == 'init':
            if device == Devices.voice and data == 'breakfast':
                Publish.speak("I will make you a breakfast.")
                #self.findObjectPointPublisher.publish(String("start"))
                Publish.find_object(String("start"))
                self.state = 'searchingCornflake'

        elif self.state == 'searchingCornflake':
            if device == Devices.recognition:
                Publish.speak("Searching cornflake.")
                object = []
                if data.isMove:
                    #to go closer
                    pass
                else:
                    objects = data.objects
                    for obj in objects:
                        if obj.category == self.desiredObject: #NOTE If found cornflakes if not loop until found
                            centroidVector = Vector3()
                            centroidVector.x = obj.point.x
                            centroidVector.y = obj.point.y
                            centroidVector.z = obj.point.z
                            #pickObjectPublisher.publish(centroidVector)
                            Publish.find_object(centroidVector)
                            #TODO debug by push out of 'if state'
                    self.state = 'graspingCornflake'

        elif self.state == 'graspingCornflake':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'trackingBowl'

        elif self.state == 'trackingBowl':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                #TODO subscribe position from camera (Color Detect)  **add color_detector to launch file
                Publish.set_manipulator_point(data)
                #Done publish position Vector3 to manipulate
                Publish.speak("pouring.")
                self.state = 'discardCornflake'

        elif self.state == 'discardCornflake':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("discard cornflake.")
                #TODO manipulate drop action isn't it?
                Publish.set_manipulator_action('walking_for_drop')
                self.state = 'searchingMilk'

        elif self.state == 'searchingMilk':
            if device == Devices.manipulator and data == 'finish':
                if device == Devices.recognition:
                    Publish.speak("Searching milk")
                    object = []
                    if data.isMove:
                        #to go closer
                        pass
                    else:
                        objects = data.objects
                        for obj in objects:
                            if obj.category == desiredObject2:
                                centroidVector = Vector3()
                                centroidVector.x = obj.point.x
                                centroidVector.y = obj.point.y
                                centroidVector.z = obj.point.z
                                Publish.set_manipulator_point(centroidVector)
                                #pickObjectPublisher.publish(centroidVector)
                                self.state = 'graspingMilk'

        elif self.state == 'graspingMilk':
            if device == Devices.manipulate and data == 'finish':
                self.state = 'trackingBowl_2'

        elif self.state == 'trackingBowl_2':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                #TODO Could we use the first point? and shall we?
                # send_object_point.publish(data)
                Publish.set_manipulator_point(data)
                Publish.speak("pouring.")
                self.state = 'discardMilk'

        elif self.state == 'discardMilk':
            if device == Devices.manipulate and data == 'finish':
                #TODO this is a pour command isn't it?
                #Publish.set_manipulator_action('walking_for_drop')
                self.state = 'serve'

        elif self.state == 'serve':
            if device == Devices.manipulate and data == 'finish':
                Publish.speak("the breakfast is ready served.")
                #TODO this is a discard command isn't it?
                Publish.set_manipulator_action('walking_for_drop')
            self.state = 'drop'

        elif self.state == 'drop':
            if device == Devices.manipulator and data == 'finish':
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
