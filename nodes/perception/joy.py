import rospy
from sensor_msgs.msg import Joy
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'Nicole'


class JoyInput(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('joy/joy', Joy, self.callback_joy_status)

    def callback_joy_status(self, data):
        self.broadcast(Devices.JOY, joy_array_transform(data))


def joy_array_transform(data_array):
    output = []
    dict = ['A', 'B', 'X', 'Y', 'LB', 'RB', 'BACK', 'START', 'LOG', 'RA', 'LA']
    if data_array.axes[6] == 1:
        output.append('LEFT')
    elif data_array.axes[6] == -1:
        output.append('RIGHT')
    if data_array.axes[7] == 1:
        output.append('UP')
    elif data_array.axes[7] == -1:
        output.append('DOWN')
    if data_array.axes[2] < 0:
        output.append('LEFT_TRIGGER')
    if data_array.axes[5] < 0:
        output.append('RIGHT_TRIGGER')

    for x in range(0, 11):
        if bool(data_array.buttons[x]):
            output.append(dict[x])
    return output

    # Don't forget to add this perception into perception_module