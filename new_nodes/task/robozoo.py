import rospy
from include.abstract_task import AbstractTask
from math import sqrt
from subprocess import call
from geometry_msgs.msg import Vector3

__author__ = 'nicole'


class RoboZoo(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'Say').say('Please come in front of me and say "follow me".')
            self.change_state('waiting_for_command')

        elif self.state is 'waiting_for_command':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.change_state('follow_init')
            elif perception_data.device is self.Devices.JOY:
                side = None
                if 'RIGHT_TRIGGER' in perception_data.input:
                    side = RIGHT
                elif 'LEFT_TRIGGER' in perception_data.input:
                    side = LEFT
                else:
                    side = None

                if side is not None:
                    if 'X' in perception_data.input:
                        # ถือพาน
                        pass
                    elif 'Y' in perception_data.input:
                        # ไหว้
                        pass
                    elif 'UP' in perception_data.input:
                        rospy.Publisher('/dynamixel/' + side, Float64).pub
                    elif 'DOWN' in perception_data.input:
                        rospy.Publisher('/dynamixel/' + side, Float64).pub
                    elif 'LEFT' in perception_data.input:
                        rospy.Publisher('/dynamixel/' + side, Float64).pub
                    elif 'RIGHT' in perception_data.input:
                        rospy.Publisher('/dynamixel/' + side, Float64).pub

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE:
                self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                distance = 9999.0  # set to maximum
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
                min_distance = 0.7  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = self.get_distance(person.personpoints, self.follow.last_point)
                    if person.personpoints.x >= self.follow.last_point.x - 0.3 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.change_state('wait_for_command')

    @staticmethod
    def get_distance(point_a, point_b):
        return sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)

RIGHT = 'right'
LEFT = 'left'
