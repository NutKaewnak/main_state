__author__ = 'AThousandYears'
import rospy

from include.abstract_subtask import AbstractSubtask
from math import atan


class FollowPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')

    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'follow' and perception_data.device is self.Devices.PEOPLE:
            rospy.loginfo("Track Person id %d", self.person_id)
            point = None
            for person in perception_data.input:
                if person.id == self.person_id:
                    point = person.personpoints
            if point is not None:
                theta = atan(point.x/point.y) 
                self.move.set_position(point.x, point.y, theta)
            else:
                rospy.loginfo("Stop Robot")
                self.move.stop()
                    
        
