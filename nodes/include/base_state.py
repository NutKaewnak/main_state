#!usr/bin/env python
import rospy
import roslib
from std_msgs.msg import String
from delay import *
from publish import *
roslib.load_manifest('main_state')




class Devices:
    door = 'door'
    base = 'base'
    manipulator = 'manipulator'
    voice = 'voice'


class BaseState:
    def __init__(self):
        rospy.Subscriber('/door/is_open', String, self.CallbackDoor)
        rospy.Subscriber('/base/is_fin', String, self.CallbackBase)
        rospy.Subscriber('/manipulator/is_fin', String, self.CallbackManipulator)
        rospy.Subscriber('/voice/output', String, self.CallbackVoice)

        self.delay = Delay()
        self.location_list = {}
        read_location(self.location_list)
        self.state = 'init'

    def callback_door(self, data):
        self.main(Devices.door, data.data)

    def callback_base(self, data):
        self.main(Devices.base, data.data)

    def callback_manipulator(self, data):
        self.main(Devices.manipulator, data.data)

    def callback_voice(self, data):
        self.main(Devices.voice, data.data)

    def main(self, device, data):
        pass

    def move_robot(self, location):
        Publish.move_absolute(self.location_list[location].pose)


if __name__ == '__main__':
    try:
        BaseState()
    except Exception, error:
        print str(error)
	
