__author__ = 'AThousandYears'
import rospy
from include.abstract_task import AbstractTask
from math import sqrt
from subprocess import call
from geometry_msgs.msg import Vector3


class Restaurant(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.location_list = {'table a': [], 'table c': [], 'table b': []}
        self.command = None
        self.count = 0
        self.first = None
        self.skill = None
        self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')

    def perform(self, perception_data):
        rospy.loginfo('state : ' + self.state + str(perception_data.input))
        if self.state is 'init':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('I will follow you.')
                self.change_state('follow_init')

        elif self.state is 'follow_init':
            if self.skill.state is not 'finish': return
            if perception_data.device is self.Devices.PEOPLE:
                distance = 2.0  # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.follow.set_person_id(id)
                    self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if self.skill.state is not 'finish': return
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 0.7  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = self.get_distance(person.personpoints, self.follow.last_point)
                    if distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('Where is this place ?')
                self.change_state('ask_for_location')
            elif perception_data.device is self.Devices.VOICE and 'robot wait' in perception_data.input and 'command' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('Wait for command.')
                self.change_state('wait_for_command')

        elif self.state is 'ask_for_location':
            if self.skill.state is not 'finish': return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location
                        self.skill = self.subtaskBook.get_subtask(self, 'Say')
                        self.skill.say('This is ' + location + ' yes or no ?')
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if self.skill.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                self.change_state('init')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

        elif self.state is 'wait_for_command':
            if self.skill.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = location
                        self.skill = self.subtaskBook.get_subtask(self, 'Say')
                        self.skill.say('go to ' + self.command + ' yes or no ?')
                        self.change_state('confirm_command')

        elif self.state is 'confirm_command':
            if self.skill.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('I will go to ' + self.command + '.')
                self.move = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.move.set_position(self.location_list[self.command][0], self.location_list[self.command][1], self.location_list[self.command][2])
                self.change_state('move_to_first')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.skill = self.subtaskBook.get_subtask(self, 'Say')
                self.skill.say('Sorry , What did you say ?')
                self.change_state('wait_for_command')

        elif self.state is 'move_to_first':
            if self.move.state is not 'finish':
                self.change_state('wait_for_order')

        elif self.state is 'wait_for_order':
            if perception_data.device is self.Devices.VOICE:
                self.skill.say('you want ' + perception_data.input + ' yes or no ?')
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = location
                        self.skill.say('go to ' + self.command + ' yes or no ?')
                        self.change_state('confirm_command')
                
    def get_distance(self, point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

