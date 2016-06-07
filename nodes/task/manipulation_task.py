import rospy
import roslib
from include.abstract_task import AbstractTask
from include.delay import Delay
from subprocess import call
from std_msgs.msg import Float64

__author__ = 'Nicole'


class ManipulationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.object_array = []
        self.number_object_found = 0
        self.delay = Delay()
        self.latex = None
        self.is_make_latex = False
        self.pub = rospy.Publisher('/dynamixel/prismatic_controller/command', Float64, queue_size=10)

    def perform(self, perception_data):
        if perception_data.device == 'HEIGHT':
            print perception_data.input
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'SetHeightRelative')
            self.pub.publish(0.0)
            self.change_state('prepare_to_recognition')

        elif self.state is 'prepare_to_recognition':
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectRecognition')
            self.delay.wait(20)
            self.change_state('recognition_object_on_1st_plane')

        elif self.state is 'recognition_object_on_1st_plane':
            if self.subtask.state is 'save_object':
                found_object = self.subtask.get_object()
                self.object_array.append(found_object)
                self.to_pdf(self.subtask.get_object())
                self.number_object_found += 1
                rospy.loginfo('Found: '+self.number_object_found+' '+object)

                if self.number_object_found == 5:
                    self.change_state('finish_1_plane')
                else:
                    self.subtask.refind()

            if self.delay.is_waiting() is False:
                self.change_state('finish_1_plane')

        elif self.state is 'finish_1_plane':
            self.subtask = self.subtaskBook.get_subtask(self, 'SetHeightRelative')
            self.pub.publish(0.1)
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectRecognition')
            self.delay.wait(20)
            self.number_object_found = 0
            self.change_state('recognition_object_on_2_plane')

        elif self.state is 'recognition_object_on_2_plane':
            if self.subtask.state is 'save_object':
                found_object = self.subtask.get_object()
                self.object_array.append(found_object)
                self.to_pdf(self.subtask.get_object())
                self.number_object_found += 1
                rospy.loginfo('Found: '+self.number_object_found+' '+object)

                if self.number_object_found == 5:
                    self.change_state('finish_2_plane')
                else:
                    self.subtask.refind()

            if self.delay.is_waiting() is False:
                self.change_state('finish_2_plane')

        elif self.state is 'finish_2_plane':
            self.subtask = self.subtaskBook.get_subtask(self, 'SetHeightRelative')
            self.pub.publish(0.2)
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectRecognition')
            self.delay.wait(20)
            self.number_object_found = 0
            self.change_state('recognition_object_on_3_plane')

        elif self.state is 'recognition_object_on_3_plane':
            if self.subtask.state is 'save_object':
                found_object = self.subtask.get_object()
                self.object_array.append(found_object)
                self.to_pdf(self.subtask.get_object())
                self.number_object_found += 1
                rospy.loginfo('Found: '+self.number_object_found+' '+object)

                if self.number_object_found == 5:
                    self.change_state('finish_3_plane')
                else:
                    self.subtask.refind()

            if self.delay.is_waiting() is False:
                self.change_state('finish_3_plane')

        elif self.state is 'finish_3_plane':
            self.subtask = self.subtaskBook.get_subtask(self, 'SetHeightRelative')
            self.pub.publish(0.3)
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectRecognition')
            self.delay.wait(20)
            self.number_object_found = 0
            self.change_state('finish_detect')

        elif self.state is 'finish_detect':
            self.on_end_latex()
            self.subtaskBook.get_subtask(self, 'Say').say('I\'m finish detecting')
            self.change_state('prepare_to_pick_object')

        elif self.state is 'prepare_to_pick_object':
            # self.subtask = self.subtaskBook.get_subtask(self, 'PickObject')
            self.change_state('pick_object')

        elif self.state is 'pick_object':
            if self.number_object_found is 0:
                self.change_state('finish')
            else:
                # self.subtask.pick(self.object_array[self.number_object_found])  # this subtask is not created
                rospy.loginfo('Picking ' + self.object_array[self.number_object_found])
                if self.subtask.state is 'finish':
                    self.number_object_found -= 1
