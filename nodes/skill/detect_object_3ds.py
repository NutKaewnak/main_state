from include.abstract_skill import AbstractSkill
from include.move_base_status import MoveBaseStatus

__author__ = "Frank"


class DetectObject3Ds(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.objects = None

    def detect(self):
        self.change_state('active')
        self.controlModule.object_3d_detector.set_new_goal()

    def perform(self, perception_data):
        # print 'state_object_skill = ' + self.state
        if self.state is 'active':
            # check if base succeed
            # print 'state_object_skill = ' + self.state
            if perception_data.device is self.Devices.OBJECT_3DS_DETECTOR:
                # print 'input= '+str(perception_data.input)
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                # print 'state_object_skill 222= ' + self.state
                self.change_state(status)
                # print 'state_object_skill = ' + self.state

            if self.state is 'succeeded':
                if not perception_data.input.result.objects:
                    self.change_state('not_found')
                self.objects = perception_data.input.result.objects

                    # print self.objects
