__author__ = 'nicole'
import rospy
import roslib
from include.abstract_subtask import AbstractSubtask
from manipulator.srv import *


class Grab(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.isGrab_able = None
        self.man_service = None
        self.x = None
        self.y = None
        self.z = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.x = None
            self.y = None
            self.z = None

        elif self.state is 'unableToGrab':
            # move closer to position self.x self.y self.z
            rospy.loginfo('foundObject')
            self.grab(self.x, self.y, self.z)

    def grab_point(self, point):
        self.grab(point.x, point.y, point.z)

    def grab(self, x, y, z):
        # x y z from shoulder waiting Joe to transform point to base
        self.x = x
        self.y = y
        self.z = z
        self.isGrab_able = None
        rospy.wait_for_service('isManipulable')
        try:
            self.man_service = rospy.ServiceProxy('isManipulable', manipulator_S)
            self.isGrab_able = self.man_service(self.x, self.y, self.z)
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
            self.change_state('error')
        if self.isGrab_able is False:
            self.change_state('unableToGrab')
        else:
            self.change_state('finish')

        # Don't forget to add this subtask to subtask book