import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class template(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'init':
            # check if skill is succeed
            if self.skill.state is 'succeed':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                rospy.loginfo('Aborted at MovePassDoor')
                self.change_state('error')

# Don't forget to add this subtask to subtask book