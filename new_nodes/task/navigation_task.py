__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay


class NavigationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state_with_subtask('move_pass_door', 'MovePassDoor')

        elif self.state is 'move_pass_door':
            rospy.loginfo('going to waypoint 1')
            self.delay.period(90)
            self.subtask = self.subtaskBook.get_subtask('MoveToLocation')
            self.subtask.toLocation('waypoint 1')  # must change
            self.change_state('going_to_waypoint1')

        elif self.state is 'going_to_waypoint1':
            if self.subtask.state is 'finish' or self.delay.is_waiting() is False:
                self.change_state('prepare_to_waypoint2')
            elif self.subtask.state is 'error aborted':
                self.subtask.toLocation('waypoint 1')  # must change

        elif self.state is 'prepare_to_waypoint2':
            self.delay.period(150)
            self.subtask.toLocation('waypoint 2')  # must change
            self.change_state('going_to_waypoint2')

        elif self.state is 'going_to_waypoint2':
            if self.subtask.state is 'finish' or self.delay.is_waiting() is False:
                self.change_state('prepare_to_waypoint3')
            elif self.subtask.state is 'error aborted':
                self.subtask = self.subtaskBook.get_subtask('MoveRelative')
                self.subtask.set_postion(-2, 0, 0)



            self.change_state('finish')
            # Don't forget to add task to task_book
            # Don't forget to create launch file
