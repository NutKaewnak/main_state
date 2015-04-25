__author__ = 'nicole'
from include.abstract_task import AbstractTask


class Cocktail(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.objective = 'getOrder'
        self.personNameList = []
        self.objectList = []

    def perform(self, perception_data):
        if self.state is 'init':
            if self.state is 'init':
                self.change_state_with_subtask('movePassDoor', 'MovePassDoor')

        elif self.state is 'movePassDoor' or self.state is 'findAnotherOrder':
            self.subtask = self.change_state_with_subtask('gotoKitchenRoom', 'MoveToLocation')
            if self.subtask is not None:
                self.subtask.to_location('kitchen counter')

        elif self.state is 'gotoKitchenRoom':
            if self.subtask.stage is 'finish':
                if self.objective is 'getOrder':
                    self.subtask = self.subtaskBook.get_subtask(self, 'FindPeopleUsingGesture')  # must make it
                elif self.objective is 'serveOrder':
                    self.subtask = self.change_state_with_subtask('searchPeople', 'CallPeopleAndFindUsingGesture')
                    if self.subtask is not None:
                        self.subtask.callFor(self.personNameList[0])
                else:
                    self.change_state('searchPeople')

        elif self.state is 'searchPeople':
            if self.subtask.stage is 'finish':
                person = self.subtask.getFoundPerson()
                if person is None:
                    self.change_state('error')
                self.subtask = self.change_state_with_subtask('getToPerson', 'MoveToPerson')  # must make it
                if self.subtask is not None:
                    self.subtask.ToPerson(person)

        elif self.state is 'getToPerson':
            if self.subtask.stage is 'finish':
                self.subtask = None
                if self.objective is 'getOrder':
                    self.subtask = self.change_state_with_subtask('askForCommand', 'AskForCommand')  # must make it
                elif self.objective is 'serveOrder':
                    self.subtask = self.change_state_with_subtask('serve', 'ServeOrder')  # must make it

        elif self.state is 'askForCommand':
            if self.subtask.state is 'finish':
                if (self.subtask.getName() is not None
                        and self.subtask.getObject() is not None):
                    self.personNameList.append(self.subtask.getName())
                    self.objectList.append(self.subtask.getObject())
                else:
                    self.change_state('error')

                if len(self.personNameList) < 3:
                    self.change_state('findAnotherOrder')
                else:
                    self.subtask = None
                    self.subtask = self.change_state_with_subtask('goGetObject', 'MoveToLocation')
                    if self.subtask is not None:
                        self.subtask.to_location('hallway table')

        elif self.state is 'goGetObject':
            if self.subtask.state is 'finish':
                if len(self.objectList) > 0:
                    self.objective = 'serveOrder'
                    self.subtask = self.change_state_with_subtask('grabObject', 'Grab')  # must make it
                    if self.subtask is not None:
                        self.subtask.grab(self.objectList[0])
                else:
                    self.change_state_with_subtask('finish', 'LeaveArena')


        elif self.state is 'grabObject':
            if self.subtask.state is 'finish':
                self.subtask = self.change_state_with_subtask('gotoKitchenRoom', 'MoveToLocation')
                if self.subtask is not None:
                    self.subtask.to_location('kitchen counter')

        elif self.state is 'serve':
            if self.subtask.state is 'finish':
                self.personNameList.pop(0)
                self.objectList.pop(0)
                self.change_state('goGetObject')