__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask


class TestFindPerson(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            self.subtask = self.subtaskBook.get_subtask(self, 'PeopleDetect')
            self.change_state('performing')

        elif self.state is 'performing':
            if self.subtask.is_found is True:
                rospy.loginfo('found' + str(self.subtask.nearest_people))
            if self.subtask.state is 'not_found':
                self.change_state('finish')