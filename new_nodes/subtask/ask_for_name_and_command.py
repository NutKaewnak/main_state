__author__ = 'nicole'


from include.abstract_subtask import AbstractSubtask


class AskForNameAndCommand(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.person = None
        self.order = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.person = None
            self.order = None
            self.subtask = self.subtaskBook.get_subtask(self, 'AskForName')
            self.change_state('askForName')

        elif self.state is 'askForName':
            if self.current_subtask.state is 'finish':
                self.person = self.current_subtask.getPerson()
                self.subtaskBook.get_subtask(self, 'askForCommand')
                self.change_state('askForObject')

        elif self.state is 'askForObject':
            if self.current_subtask.state is 'finish':
                self.order = self.current_subtask.getOrder()
                self.change_state('finish')

    def getObject(self):
        return self.order

    def getPerson(self):
        return self.person

# Don't forget to add this subtask to subtask book