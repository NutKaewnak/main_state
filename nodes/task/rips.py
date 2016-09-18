__author__ = "AThousandYears"

import rospy
from include.delay import Delay
from include.abstract_task import AbstractTask


class RIPS(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.move = None
        self.delay = Delay()
        self.subtask = None

    def perform(self, perception_data):
        # print self.state
        if self.state is 'init' and perception_data.device is self.Devices.STATE_FLOW:
            self.subtaskBook.get_subtask(self, 'Say').say('I\'m ready to start')
            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            # self.delay.wait(13)
            self.change_state('movePassDoor')
            # self.change_state('qr_check')
   
        elif self.state is 'movePassDoor':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                # self.subtask.to_location('check_point')
                self.subtask.set_position(2,0,0)
                self.change_state('moveToCheckpoint')


        elif self.state is 'moveToCheckpoint':
            print self.subtask.state
            if self.current_subtask.state is 'finish':
                # self.delay.wait(15)
                self.subtaskBook.get_subtask(self, 'Say').say('I\'m ready to read')
                self.change_state('qr_check')
            elif self.current_subtask.state is 'error':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('check_point')

        elif self.state is 'qr_check':
            if perception_data.device is 'VOICE' and perception_data.input:
                # print perception_data.input
                print 'continue' in perception_data.input
                if 'continue' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                    self.subtask.to_location('exit_arena')
                    self.change_state('exit')
        #
        # elif self.stateis 'exit':
        #     if
        elif self.state is 'moveArm':
            subtask = self.change_state_with_subtask('moveToTable', 'MoveToLocation')
            if subtask is not None:
                subtask.to_location('outside_pos')
                self.change_state('finish')