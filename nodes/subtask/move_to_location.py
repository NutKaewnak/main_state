import rospy
from geometry_msgs.msg import Vector3
from include.abstract_subtask import AbstractSubtask
from include.location_information import *
from include.location_information import read_location_information
from include.object_information import read_object_info

__author__ = "AThousandYears"


class MoveToLocation(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.location = None
        self.move = None
        self.location_list = {}
        read_location_information(self.location_list)
        self.object_info = read_object_info()

    def to_location(self, location_name):
        self.location = location_name
        rospy.loginfo('Move to '+location_name)
        location_point = self.location_list[location_name].position
        # print location_point
        self.move = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
        self.move.set_position(location_point.x, location_point.y, location_point.theta)
        self.change_state('move')

    def perform(self, perception_data):
        print '9999999999999999'
        if self.state is 'move':
            # check if base succeed
            if self.move.state is 'succeeded':
                self.location = None
                self.change_state('finish')
            elif self.move.state is 'aborted':
                self.to_location(self.location)
                self.change_state('error aborted')
