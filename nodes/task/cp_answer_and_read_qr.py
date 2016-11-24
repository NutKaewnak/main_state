from include.abstract_task import AbstractTask
from include.delay import Delay
from include import answer_question_cp, qr_read_cp, arm_control
import rospkg
from std_srvs.srv import Empty
import rospy
import os
__author__ = 'cindy'


class CPAnswerAndReadQR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init' and perception_data.device is self.Devices.STATE_FLOW:
            print 'before service'
            rospy.wait_for_service('/recognizer_grammar/mic_control_open')
            rospy.wait_for_service('/recognizer_grammar/mic_control_close')
            print 'finish wait service'
            self.mic_control_open = rospy.ServiceProxy("/recognizer_grammar/mic_control_open", Empty)
            self.mic_control_close = rospy.ServiceProxy("/recognizer_grammar/mic_control_close", Empty)
            print 'ServiceProxy'
            self.mic_control_close()

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
            self.mic_control_open()
            self.change_state('waiting_voice')

        elif self.state is 'waiting_voice':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if perception_data.input == 'robot answer question':
                    self.mic_control_close()
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask.play(os.path.join(self.path, 'robot_sound/openhouse_sound', 'imListening.wav'))
                    self.change_state('answer_question')
                elif perception_data.input == 'robot read q r':
                    self.mic_control_close()
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask.play(os.path.join(self.path, 'robot_sound/openhouse_sound', 'ReadQRCode.wav'))
                    self.change_state('check_qr')
                elif perception_data.input == 'robot supermarket mode':
                    self.mic_control_close()
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask.play(os.path.join(self.path, 'robot_sound/openhouse_sound', 'LiftingInSupermarket.wav'))
                    self.delay.wait(5)
                    self.change_state('lift_mode')

        elif self.state is 'answer_question':
            self.mic_control_open()
            self.change_state('listening_ques')

        elif self.state is 'listening_ques':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask.play(os.path.join(self.path, 'robot_sound/openhouse_sound',
                                               answer_question_cp.answers(perception_data.input)))
                self.delay.wait(10)
                self.change_state('direct_asking')

        elif self.state is 'direct_asking':
            if not self.delay.is_waiting():
                self.mic_control_close()
                self.change_state('ask_for_command')

        elif self.state is 'check_qr':
            if perception_data.device is 'VOICE' and perception_data.input:
                print perception_data.input
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask.play(os.path.join(self.path, 'robot_sound/openhouse_sound',
                                               qr_read_cp.answers(perception_data.input)))
                self.delay.wait(10)
                self.change_state('finish_read')

        elif self.state is 'finish_read':
            if not self.delay.is_waiting():
                self.change_state('ask_for_command')

        elif self.state is 'lift_mode' and perception_data.device is self.Devices.STATE_FLOW:
            if not self.delay.is_waiting():
                print 'close right arm'
                self.right_arm.move_right_joint([0.5, 0, 0.2, 0, 1.2, 0])
                self.right_arm.close()
                print 'close left arm'
                # self.left_arm.close()
                self.change_state('finish_lift')

        elif self.state is 'finish_lift' and perception_data.device is self.Devices.STATE_FLOW:
            self.mic_control_open()
            self.change_state('waiting_after_lift')

        elif self.state is 'waiting_after_lift':
            if perception_data.device is self.Devices.VOICE and perception_data.input:
                if 'robot supermarket mode' in perception_data.input:
                    self.right_arm.move_right_joint([0, 0, 0, 0, 1.2, 0])
                    # self.left_arm.close()
                    self.change_state('ask_for_command')
