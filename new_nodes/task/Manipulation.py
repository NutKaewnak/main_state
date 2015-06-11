__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask


class Manipulation(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.object_array = []
        self.number_object_found = 0
        self.pdf_file = None

    def perform(self, perception_data):
        if self.state is 'init':
            # self.pdf_file = something
            self.subtask = self.subtaskBook.get_subtask(self, 'Recognition')
            self.change_state('recognition_5_object')

        elif self.state is 'recognition_object_on_shelf':
            if self.subtask.isFound():
                # make subtask find
                object = self.subtask.get_object()
                self.object_array.append(object)
                # add data to pdf here
                self.subtask.get_object().to_pdf(self.pdf_file)

                self.number_object_found += 1
                rospy.loginfo('Found: '+self.number_object_found+' '+object)

            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'PickObject')
                self.change_state('pick_object')

        elif self.state is 'pick_object':
            if self.number_object_found is 0:
                self.change_state('finish')
            else:
                self.subtask.pick(self.object_array[self.number_object_found])
                rospy.loginfo('Picking ' + self.object_array[self.number_object_found])
                if self.subtask.state is 'finish':
                    self.number_object_found -= 1

            # Don't forget to add task to task_book
