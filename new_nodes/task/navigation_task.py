import math

__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay


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
            if self.current_subtask.state is 'finish':
                rospy.loginfo('going to waypoint 1')
                self.subtaskBook.get_subtask(self, 'Say').say('I will go to waypoint 1.')
                self.change_state('prepare_to_waypoint1')

        elif self.state is 'prepare_to_waypoint1':
            self.delay.wait(90)
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_1')  # must change
            self.change_state('going_to_waypoint1')

        elif self.state is 'going_to_waypoint1':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.subtaskBook.get_subtask(self, 'Say').say('I reach waypoint 1.')
                self.change_state('prepare_to_waypoint2')
            elif self.subtask.state is 'error aborted':
                rospy.loginfo('resend goal in waypoint_1')
                self.subtask.to_location('waypoint_1')  # must change

        elif self.state is 'prepare_to_waypoint2':
            rospy.loginfo('going to waypoint 2')
            self.delay.wait(150)
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('waypoint_2')  # must change
            self.change_state('going_to_waypoint2')

        elif self.state is 'going_to_waypoint2':
            if self.subtask.state is 'finish' or not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I will leaving arena')
                self.change_state('prepare_leave_arena')

            elif self.subtask.state is 'error aborted':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_postion(0, 0, math.pi)
                self.change_state('finding_obstacle_waypoint2')

        elif self.state is 'finding_obstacle_waypoint2':
            self.subtask = self.subtaskBook.get_subtask(self, 'DetectFrontPerson')  # detect if people is blocking
            if self.subtask.state is 'found':
                self.change_state('blocked_by_people')
            elif self.subtask.state is 'not_found':
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

        elif self.state is 'prepare_leave_arena':
            self.subtask = self.subtaskBook(self, 'LeaveArena')
            self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')