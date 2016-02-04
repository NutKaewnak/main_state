import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class FindPeopleAndGetOrder(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.order = None
        self.people = None
        self.state = 'init'

    def perform(self, perception_data):
        # if self.state is not 'finish':
        #     rospy.loginfo('FindPeopleAndGetOrder '+self.state)
        if self.state is 'init':
            self.order = None
            self.people = None
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('party room')
            self.change_state('moveToLivingRoom')

        elif self.state is 'moveToLivingRoom':
            if self.current_subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'DetectAndMoveToPeople')
                self.change_state('detectAndMoveToPeople')

        # TODO: Create subtask to speak some certain conversation
        elif self.state is 'detectAndMoveToPeople':
            if self.current_subtask.state is 'finish':
                self.neck.set_neck_angle(0, 0)
                self.subtask = self.subtaskBook.get_subtask(self, 'AskForNameAndCommand')
                self.change_state('askForCommand')
                rospy.loginfo('askForCommand')

        elif self.state is 'askForCommand':
            if self.current_subtask.state is 'finish':
                self.order = self.subtask.getObject()
                self.people = self.subtask.getPerson()
                if self.order is not None and self.people is not None:
                    self.change_state('finish')
                    rospy.loginfo('subtask finish')

    def get_people(self):
        return self.people

    def get_order(self):
        return self.order

# Don't forget to add this to subtask book.
