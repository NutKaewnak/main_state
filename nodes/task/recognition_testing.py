from include.abstract_task import AbstractTask
import rospy

__author__ = 'Frank'


class TestRecognition(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.recognize_objects = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo("Start Main State: Find Object, State: " + self.state)
            self.recognize_objects = self.subtaskBook.get_subtask(self, 'RecognizeObjects')
            self.recognize_objects.start(['*'])
            self.change_state('findObject')

        if self.state is 'findObject':
            if self.recognize_objects.state is 'finish':
                rospy.loginfo("Found: {0}".format(self.recognize_objects.objects))
                self.change_state('done')
