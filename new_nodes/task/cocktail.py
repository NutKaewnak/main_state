__author__ = 'nicole'
import rospy
from include.abstract_task import AbstractTask


class Cocktail(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.objective = 'getOrder'
        self.personNameList = []
        self.orderList = []

    def perform(self, perception_data):
        if self.state is 'init':
            if self.state is 'init':
                self.change_state_with_subtask('movePassDoor', 'MovePassDoor')

        elif self.state is 'movePassDoor' or self.state is 'findAnotherOrder':
            self.subtask = self.change_state_with_subtask('findPeopleAndGetOrder', 'FindPeopleAndGetOrder')

        elif self.state is 'findPeopleAndGetOrder':
            if self.current_subtask.state is 'finish':
                self.personNameList.append(self.subtask.getPeople())
                self.orderList.append(self.subtask.getOrder())

                if self.subtask.getPeople() is None or self.subtask.getOrder() is None:
                    self.change_state('error')
                    rospy.loginfo('Bug in subtask find people and get order')

                if len(self.personNameList) >= 3:
                    self.change_state('prepareToServePerson')
                else:
                    rospy.loginfo('got : '+str(len(self.personNameList))+' persons')
                    if self.current_subtask.state is 'finish':
                        self.subtask.change_state('init')

        elif self.state is 'prepareToServePerson':
            # self.subtask = self.change_state_with_subtask('getObjectAndServePerson', 'GrabObjectToPerson')
            # must make it
            self.change_state('getObjectAndServePerson')

        elif self.state is 'getObjectAndServePerson':
            if self.current_subtask.stage is 'finish':
                if len(self.personNameList) == 0 or len(self.orderList) == 0:
                    rospy.loginfo('done serve object')
                    self.subtask = self.change_state('exit')

                person = self.personNameList.pop(0)
                order = self.orderList.pop(0)
                self.subtask.start(order, person)

        elif self.state is 'exit':
            self.change_state_with_subtask('finish', 'LeaveArena')
