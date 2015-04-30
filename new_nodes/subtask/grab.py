__author__ = 'nicole'
import rospy

from include.abstract_subtask import AbstractSubtask
from manipulator.srv import *


class Grab(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.x = None
        self.y = None
        self.z = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.x = None
            self.y = None
            self.z = None

    def grab_point(self, point):
        self.grab(point.x, point.y, point.z)

    def grab(self, x, y, z):
        # x y z from shoulder waiting Joe to transform to base
        self.x = x
        self.y = y
        self.z = z




# Don't forget to add this subtask to subtask book