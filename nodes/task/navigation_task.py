import math

import rospy
import tf
from geometry_msgs.msg import Point

from include.abstract_task import AbstractTask
from include.delay import Delay
from nodes.subtask.include.get_distance import get_distance

__author__ = 'Nicole'


class NavigationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.delay = Delay()
        self.follow = None
        self.is_people_blocked_waypoint_2 = False
        self.tf_listener = None
        self.waypoint_2 = Point()
        self.waypoint_2.x = 11.997
        self.waypoint_2.y = -6.004

    def perform(self, perception_data):
        if self.state is 'init':
            self.tf_listener = tf.TransformListener()
            rospy.loginfo('NavigationTask init')
            self.change_state_with_subtask('move_pass_door', 'MovePassDoor')

        elif self.state is 'move_pass_door':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 1')
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 1.')
                self.change_state('prepare_to_waypoint1')

        elif self.state is 'prepare_to_waypoint1':
            self.delay.wait(90)
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_1')
            self.change_state('going_to_waypoint1')

        elif self.state is 'going_to_waypoint1':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                if self.subtask.state is 'finish':
                    self.subtaskBook.get_subtask(self, 'Say').say('I reached waypoint 1.')
                elif not self.delay.is_waiting():
                    self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 2.')
                self.change_state('prepare_to_waypoint2')
            elif self.subtask.state is 'error aborted':
                rospy.loginfo('resend goal in waypoint_1')
                self.subtask.to_location('waypoint_1')

        elif self.state is 'prepare_to_waypoint2':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 2')
                self.delay.wait(150)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('pre_waypoint_2')
                self.change_state('going_to_waypoint2')

        elif self.state is 'going_to_waypoint2':
            if perception_data.device is 'PEOPLE' and perception_data.input is not []:
                for x in perception_data.input:
                    point_tf = self.tf_listener.transformPoint('odom', x)
                    distance = math.hypot(self.waypoint_2.x - point_tf.x, self.waypoint_2.y - point_tf.y)
                    if distance <= 2:
                        rospy.loginfo('Found people block the way')
                        self.is_people_blocked_waypoint_2 = True

            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                if self.is_people_blocked_waypoint_2:
                    self.change_state('blocked_by_people')
                else:
                    self.change_state('blocked_by_chair')
            elif self.subtask.state is 'error aborted':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_postion(0, 0, math.pi)
                self.change_state('move_back')

        elif self.state is 'move_back':
            if self.subtask.state is 'finish':
                self.subtask.set_postion(1.5, 0, math.pi)
                self.change_state('finding_obstacle_waypoint2')

        elif self.state is 'blocked_by_people':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('Excuse me. May I pass')
            self.change_state('enter_waypoint2')

        elif self.state is 'blocked_by_chair':
            # TODO: implement arm here!
            self.change_state('enter_waypoint2')

        elif self.state is 'enter_waypoint2':
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.toLocation('waypoint_2')
            self.change_state('wait_enter_waypoint2')

        elif self.state is 'wait_enter_waypoint2':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I will go to waypoint 3')
                self.change_state('prepare_to_waypoint3')

        elif self.state is 'prepare_to_waypoint3':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 3')
                self.delay.wait(150)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_3')  # must change
                self.change_state('going_to_waypoint3')

        elif self.state is 'going_to_waypoint3':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'FollowPerson')
                self.change_state('prepare_follow')

        elif self.state is 'prepare_follow':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                self.change_state('follow_init')

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE:
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
                    if person.personpoints.x >= self.follow.last_point.x - 0.25 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            if self.subtask.state is 'abort':
                self.change_state('prepare_leave_arena')

        elif self.state is 'prepare_leave_arena':
            rospy.loginfo('leave arena')
            self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
            self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')
