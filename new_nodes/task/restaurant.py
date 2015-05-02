__author__ = 'AThousandYears'
import rospy
from include.abstract_task import AbstractTask
from math import sqrt
from subprocess import call


class Restaurant(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.location_list = {'location one': [], 'location two': [], 'location three': [],
                              'snack shelf': [], 'food shelf': [], 'drink shelf': []}
        self.command = None
        self.count = 0
        self.first = None

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
                    if distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                call(['espeak', '-ven+f4', 'Where is this place ?', '-s 120'])
                self.change_state('ask_for_location')
            elif perception_data.device is self.Devices.VOICE and 'robot halting' in perception_data.input:
                call(['espeak', '-ven+f4', 'Wait for command', '-s 120'])
                self.change_state('wait_for_command')

        elif self.state is 'ask_for_location':
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location
                        call(['espeak', '-ven+f4', 'This is ' + location + ' yes or no ?', '-s 120'])
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                call(['espeak', '-ven+f4', 'I remember ' + self.location + '.', '-s 120'])
                self.location_list[self.location] = self.perception_module.base_status.position
                self.first = self.perception_module.base_status.position
                self.change_state('init')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                call(['espeak', '-ven+f4', 'Sorry , Where is this place ?', '-s 120'])
                self.change_state('ask_for_location')

        elif self.state is 'wait_for_command':
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = perception_data.input
                        call(['espeak', '-ven+f4', self.command + ' yes or no ?', '-s 120'])
                        self.change_state('confirm_command')

        elif self.state is 'confirm_command':
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                call(['espeak', '-ven+f4', 'I will do it.', '-s 120'])
                self.count += 1
                if self.count >= 3:
                    self.change_state('move_to_first')
                else:
                    self.change_state('wait_for_command')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                call(['espeak', '-ven+f4', 'Sorry , What did you say ?', '-s 120'])
                self.change_state('wait_for_command')

        elif self.state is 'move_to_first':
            self.move = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            self.move.set_position(self.first[0], self.first[1], self.first[2])
                
    def get_distance(self, point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

