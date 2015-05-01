__author__ = "AThousandYears"

import rospy
from geometry_msgs.msg import Vector3

from include.abstract_subtask import AbstractSubtask


class MoveToLocation(AbstractSubtask):
    init = Vector3(4.451, 2.501, -1.389)
    pickPlace = Vector3(4.971, -1.053, -1.409)
    final = Vector3(5.918, -7.316, -1.368)
    question = Vector3(6.007, -8.220, -1.358)
    exit = Vector3(2.382, -12.863,  0.146)


    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.move = None
        self.location = None
        self.LocationList = dict()  # Must be remove after crysis zone
        self.LocationList['init'] = self.init
        self.LocationList['pickPlace'] = self.pickPlace
        self.LocationList['final'] = self.question
        self.LocationList['exit'] = self.exit
        self.LocationList['livingRoom'] = self.question
        self.LocationList['kitchenTable'] = self.exit

    def to_location(self, location_name):
        self.location = location_name
        rospy.loginfo('Move to '+location_name)
        location_point = self.get_location_point(location_name)
        self.move = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
        self.move.set_point(location_point)
        self.change_state('move')

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if self.move.state is 'succeeded':
                self.location = None
                self.change_state('finish')
            elif self.move.state is 'aborted':
                rospy.loginfo('Aborted at MovePassDoor')
                self.to_location(self.location)
                self.change_state('error')

    def get_location_point(self, location_name):
        return self.LocationList[location_name]
