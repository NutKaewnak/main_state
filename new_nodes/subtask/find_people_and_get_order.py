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
        if self.state is 'init':
            self.order = None
            self.people = None
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.To_Location('LivingRoom')
            self.change_state('moveToLivingRoom')

        elif self.state is 'moveToLivingRoom':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'FindPeopleUsingGesture')  # must make it
                self.change_state('findPeople')

        elif self.state is 'findPeople':
            if self.subtask.state is 'finish':
                pos = self.subtask.getPos()
                self.subtask = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
                self.subtask.setPoint(pos)
                self.change_state('moveToPeople')

        elif self.change_state('moveToPeople'):
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'AskForNameAndCommand')  # must make it
                self.change_state('askForCommand')

        elif self.state is 'askForCommand':
            if self.subtask.state is 'finish':
                self.order = self.subtask.getOrder()
                self.people = self.subtask.getPeople()
                self.change_state('finish')

    def getPeople(self):
        return self.people

    def getOrder(self):
        return self.order

# Don't forget to add this to subtask book.