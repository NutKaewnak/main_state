from include.abstract_skill import AbstractSkill
from include.arm_status import ArmStatus
__author__ = 'nicole'


class ArmStaticPose(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.arm = None
        self.device = None

    def perform(self, perception_data):
        if self.state is 'receive_pose':
            if perception_data.device is self.device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                print state
                self.change_state(state)

    def static_pose(self, pose):
        """

        :param pose: (str)
        :return: None
        """
        print pose
        if 'right' in pose:
            self.arm = self.controlModule.right_arm
            self.device = 'RIGHT_ARM'
        elif 'left' in pose:
            self.arm = self.controlModule.left_arm
            self.device = 'LEFT_ARM'
        self.arm.init_controller()
        self.arm.static_pose(pose)
        self.change_state('receive_pose')
