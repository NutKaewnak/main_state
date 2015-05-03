__author__ = 'AThousandYears'
import rospy
from include.abstract_task import AbstractTask
from math import sqrt


class FollowMe(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.change_state('follow_init')

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE:
                self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                distance = 9999.0 # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
                    self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 0.7 # set to maximum
                id = None
                for person in perception_data.input:
                    distance = self.get_distance(person.personpoints, self.follow.last_point)
                    if distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'leave elevator' in perception_data.input:
                self.move = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.move.set_position(-3.0, 0, -3.1415)
                self.change_state('leave_elevator')
        elif self.state is 'leave_elevator':
            pass
            
                
    def get_distance(self, point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)
