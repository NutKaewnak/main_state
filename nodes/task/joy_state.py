from include.abstract_task import AbstractTask
import rospkg
import os

__author__ = 'cindy'


class JoyState(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask_name = None
            rospack = rospkg.RosPack()
            self.path = rospack.get_path('main_state')
            self.change_state("wait_joy")

        if self.state is 'wait_joy':
            if perception_data.device is self.Devices.JOY and perception_data.input:
                print 'input ', perception_data.input
                if 'B' in perception_data.input and 'LB' in perception_data.input:
                    print 'B'
                    # self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    # self.subtask.say('hi')
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask_name = 'PlaySound'
                    # print self.subtask
                    self.subtask.play(os.path.join(self.path, 'sound', 'duck.wav'))
                    self.change_state('doing')
                elif 'A' in perception_data.input:
                    print 'A'
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('hello')
                    self.change_state('doing')
                elif 'X' in perception_data.input:
                    print 'X'
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('Lumyai')
                    self.change_state('doing')
                elif 'Y' in perception_data.input:
                    print 'Y'
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('wow')
                    self.change_state('doing')

        elif self.state is 'doing':
            if perception_data.device is self.Devices.JOY and 'RB' in perception_data.input \
                    and 'RIGHT_TRIGGER' in perception_data.input:
                # print dir(self.subtask.subtaskBook)
                if self.subtask_name == 'PlaySound':
                    self.subtask.terminate_sound()
                    self.subtask_name = None
                # print '----------------terminate------------------'
            if self.subtask.state is 'finish' or self.subtask.state is 'aborted':
                print '1'
                self.change_state('wait_joy')
