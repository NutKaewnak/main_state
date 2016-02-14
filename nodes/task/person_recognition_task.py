__author__ = 'Nicole'
import math
from random import randrange
from include.abstract_task import AbstractTask


class PersonRecognitionTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.person = None

    def perform(self, perception_data):
        if self.state is 'init':
            # prepare to memorize operator
            self.subtask = self.subtaskBook.get_subtask(self, 'Introduce')
            self.change_state('memorizing_operator')

        elif self.state is 'memorizing_operator':
            # get operator name
            # memorize operator face
            # wait for command
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            # if command == 'start'
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
            self.subtask.set_position(0, 0, math.pi)  # turn 180
            self.change_state('search_for_crowd')

        elif self.state is 'search_for_crowd':
            # looking for crowd between 2-3 m.
            # crowd is between 5-10 people
            # implement people detect only first
            self.change_state('find_the_operator')

        elif self.state is 'find_the_operator':
            # walk in front of operator
            self.change_state('walk_to_operator')

        elif self.state is 'walk_to_operator':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('I found you operator')  # say 'I found you operator(name)

            # state operator gender (if possible)
            random = randrange(100)
            if random < 70:
                self.subtask.say('You are male')
            else:
                self.subtask.say('You are female')

            # state operator pose (if possible)
            self.change_state('state_the_crowd')

        elif self.state is 'state_the_crowd':
            # state crowd size ( 5-10 people )
            # state number of men
            # state number of women
            self.change_state('finish')

            # Don't forget to add task to task_book
            # Don't forget to create launch file