__author__ = 'Nicole'

from include.abstract_skill import AbstractSkill
from include.arm_status import ArmStatus
from include.delay import Delay


class Pick(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.manipulator = self.controlModule.manipulator
        self.side = 'right'
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('waiting_for_goal')

        elif self.state is 'prepare_to_pick':
            self.manipulator.static_pose(self.side + '_arm', self.side + '_normal')  # may change
            self.change_state('arm_normal')

        elif self.state is 'arm_normal':
            device = None
            if self.side is 'right':
                device = 'RIGHT_ARM'
            elif self.side is 'left':
                device = 'LEFT_ARM'
            if device is not None and perception_data.device is device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                if state is 'succeeded':
                    self.change_state('prepare_move_hand_to_front_of_object')

        elif self.state is 'prepare_move_hand_to_front_of_object':
            self.change_state('move_to_in_front_of_object')

        elif self.state is 'move_to_in_front_of_object':
            self.change_state('prepare_to_open_gripper')

        elif self.state is 'prepare_to_open_gripper':
            self.change_state('open_gripper')

        elif self.state is 'open_gripper':
            self.change_state('prepare_move_to_object')

        elif self.state is 'prepare_move_to_object':
            # problem here
            self.delay.wait(5)
            self.change_state('move_to_object')

        elif self.state is 'move_to_object':
            if not self.delay.is_waiting():  # and device state is succeeded
                self.change_state('grab_object')

        elif self.state is 'grab_object':
            # close gripper
            self.change_state('succeeded')

    def pick_from_point(self, goal):
        self.change_state('init')
        self.controlModule.manipulator.manipulate('right_arm', goal)
        self.change_state('prepare_to_pick')

    def set_side(self, side):
        self.side = side