from include.abstract_task import AbstractTask
import rospy

__author__ = 'Frank'


class TestObject3DsDetection(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.objects_detection_subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo("Start Main State: Find Object, State: " + self.state)
            self.objects_detection_subtask = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
            self.objects_detection_subtask.start()
            self.change_state('findObject')

        if self.state is 'findObject':
            if self.objects_detection_subtask.state is 'finish':
                rospy.loginfo("Found: {0}".format(self.objects_detection_subtask.objects))
                self.change_state('done')
