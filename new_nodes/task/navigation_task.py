__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay
from geometry_msgs.msg import Vector3
from subprocess import call
from math import sqrt


class NavigationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.delay = Delay()
        self.follow = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('NavigationTask init')
            self.change_state_with_subtask('move_pass_door', 'MovePassDoor')

        elif self.state is 'move_pass_door':
            rospy.loginfo('going to waypoint 1')
            self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 1.')
            self.delay.wait(90)
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_1')  # must change
            self.change_state('going_to_waypoint1')

        elif self.state is 'going_to_waypoint1':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.change_state('prepare_to_waypoint2')
            elif self.subtask.state is 'error aborted':
                self.subtask.to_location('waypoint_1')  # must change

        elif self.state is 'prepare_to_waypoint2':
            rospy.loginfo('going to waypoint 2')
            self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 2.')
            self.delay.wait(150)
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_2')  # must change
            self.change_state('going_to_waypoint2')

        elif self.state is 'going_to_waypoint2':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                # self.change_state('prepare_to_waypoint3')
                self.change_state('finish')

            elif self.subtask.state is 'error aborted':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_postion(-2, 0, 0)
                self.change_state('finding_obstacle_waypoint2')

        elif self.state is 'finding_obstacle_waypoint2':
            self.subtask = self.subtaskBook.get_subtask(self, 'PeopleDetect')  # detect if people is blocking the way
            if self.subtask.is_found:
                self.change_state('blocked_by_people')
            else:
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.toLocation('waypoint 2')  # must change
                self.change_state('going_to_waypoint2')
            # cannot detect furniture yet

        elif self.state is 'blocked_by_people':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('Excuse me. May I pass')
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.toLocation('waypoint 2')  # must change
            self.change_state('going_to_waypoint2')

        elif self.state is 'prepare_to_waypoint3':
            # waiting for twist from P'Krit

            self.subtask = self.subtaskBook.get_subtask(self, 'FollowPerson')
            set_neck_angle_topic = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)
            set_neck_angle_topic.publish(Vector3())
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                call(['espeak', '-ven+f4', 'I will follow you.', '-s 120'])
                self.change_state('follow_init')

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
                    distance = get_distance(person.personpoints, self.follow.last_point)
                    if distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.change_state('prepare_to_waypoint4')

        elif self.state is 'prepare_to_waypoint4':
            self.change_state('finish')
            # Don't forget to add task to task_book
            # Don't forget to create launch file


def get_distance(point_a, point_b):
    return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)