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
        if self.state is 'active':
            # check if base succeed
            if perception_data.device is self.Devices.OBJECT_3DS_DETECTOR:
                print 'input= '+str(perception_data.input)
                print 'result.object = '+str(perception_data.input.result.objects)
                print 'result.object[0].point = '+str(perception_data.input.result.objects[0].point)
                print 'result.object[0].width = '+str(perception_data.input.result.objects[0].width)
                status = MoveBaseStatus.get_state_from_status(perception_data.input.status.status)
                self.change_state(status)
                print 'state_object = ' + self.state
                if self.state is 'succeeded':
                    if not perception_data.input.result.objects:
                        self.change_state('not_found')
                    self.objects = perception_data.input.result.objects

                    print self.objects
