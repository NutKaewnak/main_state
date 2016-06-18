from include.abstract_subtask import AbstractSubtask

__author__ = 'Frank'


class RecognizeObjects(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.objects = None
        self.recognize_objects = None

    def start(self, object_names):
        self.recognize_objects = self.skillBook.get_skill(self, 'RecognizeObjects')
        self.recognize_objects.recognize(object_names)
        self.change_state('recognizing')

    def perform(self, perception_data):
        # if self.state is 'init':
        #     self.recognize_objects = self.skillBook.get_skill(self, 'RecognizeObjects')
        #     self.change_state('recognizing')
        if self.state is 'recognizing':
            if self.recognize_objects.state is 'succeeded':
                self.objects = self.recognize_objects.objects
                self.change_state('finish')
