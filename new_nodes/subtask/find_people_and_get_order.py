__author__ = 'nicole'



import rospy

from include.abstract_subtask import AbstractSubtask


class FindPeopleAndGetOrder(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.order = None
        self.people = None

    def perform(self, perception_data):
        rospy.loginfo('FindPeopleAndGetOrder'+self.state)
        if self.state is 'init':
            self.order = None
            self.people = None
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('livingRoom')
            self.change_state('moveToLivingRoom')

        elif self.state is 'moveToLivingRoom':
            if self.current_subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'DetectAndMoveToPeople')
                self.change_state('detectAndMoveToPeople')
                rospy.loginfo('detectAndMoveToPeople')

        elif self.state is 'detectAndMoveToPeople':
            if self.current_subtask.state is 'finish':
                # self.subtask = self.subtaskBook.get_subtask(self, 'AskForNameAndCommand')  # must make it
                self.change_state('askForCommand')
                rospy.loginfo('askForCommand')

        elif self.state is 'askForCommand':
            if self.current_subtask.state is 'finish':
                self.order = 'coke'  # self.subtask.getOrder()
                self.people = 'Amanda'  # self.subtask.getPeople()
                if self.order is not None and self.people is not None:
                    self.change_state('finish')
                    rospy.loginfo('subtask finish')

    def getPeople(self):
        return self.people

    def getOrder(self):
        return self.order

# Don't forget to add this to subtask book.