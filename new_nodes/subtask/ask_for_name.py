__author__ = 'nicole'


from include.abstract_subtask import AbstractSubtask


class AskForName(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.person = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.person = None
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('Good day sir. May I know your name please.')
            self.change_state('waitingForName')

        elif self.state is 'waitingForName':
            if perception_data.device == 'VOICE':
                self.person = perception_data.input  # This line will bug for sure.

    def getPerson(self):
        return self.person