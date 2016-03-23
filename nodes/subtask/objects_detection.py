from include.abstract_subtask import AbstractSubtask

__author__ = 'Frank'


class ObjectsDetection(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.objects = None
        self.detect_object_3ds_skill = None

    def start(self):
        self.detect_object_3ds_skill = self.skillBook.get_skill(self, 'DetectObject3Ds')
        self.detect_object_3ds_skill.detect()
        self.change_state('detecting')

    def perform(self, perception_data):
        if self.state is 'detecting':
            if self.detect_object_3ds_skill.state is 'succeeded':
                self.objects = self.detect_object_3ds_skill.objects
                print 'objects_Detection'+str(self.objects)
                self.change_state('finish')
            if self.detect_object_3ds_skill.state is 'not_found':
                self.change_state('not_found')
