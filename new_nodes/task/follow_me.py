import rospy
from include.abstract_task import AbstractTask
from math import sqrt
from subprocess import call
from geometry_msgs.msg import Vector3

__author__ = 'AThousandYears'


class FollowMe(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                call(['espeak', '-ven+f4', 'I will follow you.', '-s 120'])
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
                    if person.personpoints.x >= self.follow.last_point.x - 0.3 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'robot get out' in perception_data.input:
                self.move = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.move.set_position(-3.0, 0, -1.57)
                self.change_state('leave_elevator')
        elif self.state is 'leave_elevator':
            if self.move.state is 'finish':
                call(['espeak', '-ven+f4', 'Please come in front of me.', '-s 120'])
                self.change_state('follow_init_2')
        elif self.state is 'follow_init_2':
            if perception_data.device is self.Devices.PEOPLE:
                self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                distance = 1.5 # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
                    self.change_state('follow_2')

        elif self.state is 'follow_2':
            # recovery follow
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 0.7  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = self.get_distance(person.personpoints, self.follow.last_point)
                    if person.personpoints.x >= self.follow.last_point.x - 0.3 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            if self.follow.distance_from_last <= 0.1:
                self.count += 1
                if self.count >= 100:
                    self.move = self.subtaskBook.get_subtask(self, 'MoveRelative')
                    self.move.set_position(4.0, 0, -1.57)
                    self.change_state('pass_group')
            else:
                self.count = 0
        elif self.state is 'pass_group':
            if self.move.state is 'finish':
                self.change_state('follow_init_2')
                
    def get_distance(self, point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

