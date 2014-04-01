#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from include.command_extractor import *
from math import pi

roslib.load_manifest('main_state')

class GPSR(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        rospy.loginfo('Start GPSR State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
	if self.state == 'init':
		if device == Devices.voice:
			command_extractor = CommandExtractor()
			actions = command_extractor.extractActionTuples(data)
			print actions	

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        GPSR()
    except Exception, error:
        print str(error)
