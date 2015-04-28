import rospy

__author__ = 'nicole'
from include.abstract_subtask import AbstractSubtask


class DetectAndMoveToPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.pos = None

    def perform(self, perception_data):
        if self.current_subtask is not None:
            rospy.loginfo('DetectAndMoveToPeople subtask state: '+self.current_subtask.state)
        if self.state is 'init':
            self.pos = None
            self.subtask = self.subtaskBook.get_subtask(self, 'FindPeopleUsingGesture')
            self.change_state('findPeople')

        elif self.state is 'findPeople':
            if self.current_subtask.state is 'finish':
                self.pos = self.subtask.get_point()
                self.change_state('foundPeople')
            elif self.current_subtask.state is 'notFound':
                self.skillBook.get_skill('Say').say('I can not found anyone.')
                self.change_state('notFound')

        elif self.state is 'foundPeople':
            if self.current_subtask.state is 'finish':
                self.subtask = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
                rospy.loginfo(self.pos)
                self.subtask.set_point(self.pos)
                self.change_state('moveToPeople')

        elif self.state is 'moveToPeople':
            if self.current_subtask is 'succeeded':
                self.change_state('finish')