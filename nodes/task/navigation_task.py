import math

import rospy
import tf
from geometry_msgs.msg import Point
from include.transform_point import transform_point
from include.abstract_task import AbstractTask
from include.delay import Delay
from include.get_distance import get_distance

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
        self.is_performing = False

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True

        if self.state is 'init':
            self.tf_listener = tf.TransformListener()
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.3, 0)
            rospy.loginfo('NavigationTask init')
            self.subtaskBook.get_subtask(self, 'MovePassDoor')
            # self.change_state('move_pass_door')
            self.change_state('prepare_follow')

        elif self.state is 'move_pass_door':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 1')
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 1.')
                self.change_state('prepare_to_waypoint1')

        elif self.state is 'prepare_to_waypoint1':
            self.delay.wait(90)
            self.change_state('going_to_waypoint1')
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_1')

        elif self.state is 'going_to_waypoint1':
            if self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('I reached waypoint 1.')
                self.change_state('prepare_to_waypoint2')
            elif not self.delay.is_waiting():
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 2.')
                self.change_state('prepare_to_waypoint2')

            elif self.subtask.state is 'error':
                rospy.loginfo('resend goal in waypoint_1')
                self.subtask.to_location('waypoint_1')

        elif self.state is 'prepare_to_waypoint2':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 2')
                self.change_state('going_to_waypoint2')
                self.delay.wait(150)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('pre_waypoint_2')

        elif self.state is 'going_to_waypoint2':
            if perception_data.device is 'PEOPLE' and perception_data.input is not []:
                for x in perception_data.input:
                    point_tf = transform_point(self.tf_listener, x.personpoints, 'map')
                    if point_tf:
                        distance = math.hypot(self.waypoint_2.x - point_tf.x, self.waypoint_2.y - point_tf.y)
                        print distance
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
            self.delay.wait(5)
            self.change_state('enter_waypoint2')

        elif self.state is 'blocked_by_chair':
            # TODO: implement arm here!
            self.delay.wait(5)
            self.change_state('enter_waypoint2')

        elif self.state is 'enter_waypoint2':
            if not self.delay.is_waiting():
                self.change_state('wait_enter_waypoint2')
                self.delay.wait(20)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_2')

        elif self.state is 'wait_enter_waypoint2':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I reach waypoint 2')
                self.change_state('prepare_to_waypoint3')
            elif not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I will go to waypoint 3')
                self.change_state('prepare_to_waypoint3')

        elif self.state is 'prepare_to_waypoint3':
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 3')
                self.delay.wait(150)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('waypoint_3')
                self.change_state('going_to_waypoint3')

        elif self.state is 'going_to_waypoint3':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.follow = self.subtaskBook.get_subtask(self, 'FollowMe')
                self.change_state('prepare_follow')

        elif self.state is 'prepare_follow':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.follow = self.subtaskBook.get_subtask(self, 'FollowMe')
                self.follow.start()
                self.change_state('follow_init')

        elif self.state is 'follow_init':
            if self.follow.state is 'abort':
                print 'abort'
                self.subtaskBook.get_subtask(self, 'Say').say('I will go back.')
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.state = 'finish'
                self.change_state('prepare_back_to_waypoint_3')

        elif self.state is 'prepare_back_to_waypoint_3':
            if self.subtask.state is 'finish':
                if not self.follow.goal_array:
                    self.change_state('back_to_waypoint_3')
                else:
                    self.change_state('prepare_leave_arena')

        elif self.state is 'back_to_waypoint_3':
            pose = self.follow.goal_array.pop()
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            self.subtask.set_postion(pose.x, pose.y, math.pi-pose.theta)
            self.change_state('prepare_back_to_waypoint_3')

        elif self.state is 'prepare_leave_arena':
            rospy.loginfo('leave arena')
            self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
            self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')

        self.is_performing = False
