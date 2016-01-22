from include.abstract_task import AbstractTask

__author__ = 'Frank'


class TestRecognition(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.recognize_objects = None
        # self.recognize_objects = self.subtaskBook.get_subtask(self, 'RecognizeObjects')
        # self.recognize_objects.start(['444'])
        print "create object", self.state
        # self.change_state('findObject')

    def perform(self, perception_data):
        if self.state is 'init':
            print "--init--"
            self.recognize_objects = self.subtaskBook.get_subtask(self, 'RecognizeObjects')
            self.recognize_objects.start(['444'])
            self.change_state('findObject')

        if self.state is 'findObject':
            if self.recognize_objects.state is 'finish':
                print self.recognize_objects.objects
                self.change_state('done')
