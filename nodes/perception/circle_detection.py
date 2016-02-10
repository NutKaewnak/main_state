import rospy
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from std_msgs.msg import String

__author__ = 'krit'


class CircleDetection(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber("/color_detect_output", String, self.callback_circle_detection)

        self.color = {'red': [0, 0], 'yellow': [0, 0], 'green': [0, 0]}

    def callback_circle_detection(self, data):
        output = self.track_circle(data)
        self.broadcast(Devices.CIRCLE_DETECT, output)

    def track_circle(self, data):
        output = []
        for color in self.color:
            self.track_color(data.data, color)
            if self.color[color][0] >= 10:
                output.append(color)
        return output

    def track_color(self, data, color):
        if color in data:
            self.color[color][0] += 1
        else:
            self.color[color][1] += 1

        if self.color[color][1] >= 5:
            self.color[color] = [0, 0]