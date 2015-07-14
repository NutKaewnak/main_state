__author__ = 'jamjann'
import rospy
import roslib
from include.base_state import *

names = []


def readFileToList(filename):
	output = []	
	file = open(filename)
	for line in file:
		output.append(line.strip().lower())
	return output

def toExtract(command):
	data = command.split()
	for word in data:
		if word.lower() in names:
			return word
	return None

class RecogName:
	def __init__(self):
    	BaseState.__init__(self)
    	self.names = readFileToList(roslib.packages.get_pkg_dir('main_state')+'/config/command_config/names.txt')
    	rospy.loginfo('Recognize Name State')
    	rospy.spin()

	def main(self, device, data):
		rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
		if self.state is STATE.INIT:
			if device is Devices.voice:
				name = toExtract(data) 
				self.speak("Hello, Nice to meet you "+name)

if __name__ is '__main__':
    RecogName()