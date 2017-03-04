import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'cin'


class WebCommu(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'WebCommu')

    def perform(self, perception_data):
        if self.state is 'sending':
            if self.skill.state is 'succeeded':
                self.change_state('finish')

    def send_info(self, status, table, order):
        self.skill.set_info(status, table, order)
        self.change_state('sending')



            # Don't forget to add this subtask to subtask book