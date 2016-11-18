from include.abstract_task import AbstractTask
from include.delay import Delay
from include import answer_question_cp, qr_read_cp, arm_control
import rospkg
import os
__author__ = 'cindy'


class CPAnswerAndReadQR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init' and perception_data.device is self.Devices.STATE_FLOW:
            self.delay = Delay()
            rospack = rospkg.RosPack()
            self.path = rospack.get_path('main_state')
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            self.right_arm = arm_control.RightArm()
            self.left_arm = arm_control.LeftArm()
            self.change_state('ask_for_command')

        elif self.state is 'ask_for_command' and perception_data.device is self.Devices.STATE_FLOW:
            self.subtaskBook.get_subtask(self, 'Say').say('I\'m ready for command.')
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if perception_data.input == 'robot answer question':
                    self.subtaskBook.get_subtask(self, 'Say').say('Want me to answer questions. Robot Yes or Robot No ?')
                    self.change_state('confirm_ans')
                elif perception_data.input == 'robot read q r':
                    self.subtaskBook.get_subtask(self, 'Say').say('Want me to read q r. Robot Yes or Robot No ?')
                    self.change_state('confirm_qr')
                elif perception_data.input == 'robot lift tray':
                    self.subtaskBook.get_subtask(self, 'Say').say('Want me to lift tray. Robot Yes or Robot No ?')
                    self.change_state('confirm_lift')

        elif self.state is 'confirm_ans':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if 'robot yes' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m listening.')
                    self.change_state('answer_question')
                elif 'robot no' in perception_data.input:
                    self.change_state('ask_for_command')

        elif self.state is 'confirm_qr':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if 'robot yes' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m ready for read.')
                    self.change_state('check_qr')
                elif 'robot no' in perception_data.input:
                    self.change_state('ask_for_command')

        elif self.state is 'confirm_lift':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if 'robot yes' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m lifting.')
                    self.change_state('lift_mode')
                elif 'robot no' in perception_data.input:
                    self.change_state('ask_for_command')

        elif self.state is 'answer_question':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask.play(os.path.join(self.path, 'robot_sound/cp_sound/40_QA',
                                               answer_question_cp.answers(perception_data.input)))
                self.delay.wait(10)
                self.change_state('direct_asking')

        elif self.state is 'direct_asking':
            if self.subtask.state is 'finish':
                self.change_state('ask_for_command')

        elif self.state is 'check_qr':
            if perception_data.device is 'VOICE' and perception_data.input:
                print perception_data.input
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask.play(os.path.join(self.path, 'robot_sound/cp_sound/Promotion',
                                               qr_read_cp.answers(perception_data.input)))
                self.delay.wait(10)
                self.change_state('finish_read')

        elif self.state is 'finish_read':
            if not self.delay.is_waiting():
                self.change_state('ask_for_command')

        elif self.state is 'lift_mode':
            self.right_arm.close()
            self.left_arm.close()
            self.change_state('finish_lift')

        elif self.state is 'finish_lift':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if 'robot listen command' in perception_data.input:
                    self.right_arm.close()
                    self.left_arm.close()
                    self.change_state('ask_for_command')
