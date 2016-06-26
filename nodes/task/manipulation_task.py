import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay
from include.report_generator import ReportGenerator
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped

__author__ = 'Nicole'

TOTAL_OBJECT = 5


class ManipulationTask(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.object_array = []
        self.object_array_name = []
        self.object_to_generate = []
        self.timer = Delay()
        self.report_generator = None
        self.height_pos = None
        self.height = rospy.Publisher('/dynamixel/prismatic_controller/command', Float64, queue_size=10)

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True

        if perception_data.device == 'HEIGHT':
            if perception_data.input.position != self.height_pos:
                self.height_pos = perception_data.input.position
                print 'state:', self.state
                print 'height:', perception_data.input.position

        if self.state is 'init':
            self.report_generator = ReportGenerator('Object Recognition and Manipulation')
            self.change_state('prepare_to_recognition')
            self.height.publish(0.03)
            self.timer.wait(15)

        elif self.state is 'prepare_to_recognition':
            if not self.timer.is_waiting():
                self.height.publish(self.height_pos)
                self.subtask = self.subtaskBook.get_subtask(self, 'RecognizeObjectOnPlane')
                self.subtask.found_objects = self.object_array
                self.subtask.found_objects_name = self.object_array_name
                self.change_state('recognition_object_on_1st_plane')

        elif self.state is 'recognition_object_on_1st_plane':
            if self.subtask.state is 'finish' or self.subtask.state is 'time_out':
                if len(self.object_array) >= TOTAL_OBJECT:
                    self.object_to_generate = [] + self.object_array
                    self.change_state('generate_report')
                else:
                    self.change_state('finish_1_plane')

        elif self.state is 'finish_1_plane':
            print 'len(self.object_array)', len(self.object_array)
            self.height.publish(0.08)
            self.timer.wait(5)
            self.change_state('prepare_2_plane')

        elif self.state is 'prepare_2_plane':
            if not self.timer.is_waiting():
                self.height.publish(self.height_pos)
                self.subtask = self.subtaskBook.get_subtask(self, 'RecognizeObjectOnPlane')
                self.subtask.found_objects = self.object_array
                self.subtask.found_objects_name = self.object_array_name
                self.change_state('recognition_object_on_2_plane')

        elif self.state is 'recognition_object_on_2_plane':
            if self.subtask.state is 'finish' or self.subtask.state is 'time_out':
                self.change_state('finish_detect')
                if len(self.object_array) >= TOTAL_OBJECT:
                    self.object_to_generate = [] + self.object_array
                    self.change_state('generate_report')
                else:
                    self.change_state('finish_2_plane')

        elif self.state is 'finish_2_plane':
            print 'len(self.object_array)', len(self.object_array)
            self.height.publish(0.12)
            self.timer.wait(5)
            self.change_state('prepare_3_plane')

        elif self.state is 'prepare_3_plane':
            if not self.timer.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'RecognizeObjectOnPlane')
                self.subtask.found_objects = self.object_array
                self.subtask.found_objects_name = self.object_array_name
                self.change_state('recognition_object_on_3_plane')

        elif self.state is 'recognition_object_on_3_plane':
            if self.subtask.state is 'finish' or self.subtask.state is 'time_out':
                if len(self.object_array) >= TOTAL_OBJECT:
                    self.object_to_generate = [] + self.object_array
                    self.change_state('generate_report')
                else:
                    self.change_state('finish_3_plane')

        elif self.state is 'finish_3_plane':
            print 'len(self.object_array)', len(self.object_array)
            self.height.publish(0.16)
            self.timer.wait(5)
            self.change_state('prepare_4_plane')

        elif self.state is 'prepare_4_plane':
            if not self.timer.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'RecognizeObjectOnPlane')
                self.subtask.found_objects = self.object_array
                self.subtask.found_objects_name = self.object_array_name
                self.change_state('recognition_object_on_4_plane')

        elif self.state is 'recognition_object_on_4_plane':
            if self.subtask.state is 'finish' or self.subtask.state is 'time_out':
                self.object_to_generate = [] + self.object_array
                self.change_state('generate_report')

        elif self.state is 'generate_report':
            self.timer.wait(10)
            print 'len(self.object_array)', len(self.object_array)
            while self.object_to_generate:
                print 'len(self.object_to_generate) before pop', len(self.object_to_generate)
                found_object = self.object_to_generate.pop(0)
                print 'generate report for', found_object.name.data
                self.report_generator.generate_object_report(found_object)
                print 'len(self.object_to_generate)', len(self.object_to_generate)
            self.change_state('finish_detect')

        elif self.state is 'finish_detect':
            if not self.timer.is_waiting():
                self.subtaskBook.get_subtask(self, 'Say').say('I\'m finish detecting')
                self.change_state('pick_object')
                self.report_generator.on_end_latex()

        elif self.state is 'pick_object':
            if len(self.object_array) == 0:
                self.change_state('finish')
            elif self.subtask.state is 'finish':
                self.change_state('prepare_to_pick_object')

        elif self.state is 'prepare_to_pick_object':
            if self.object_array:
                self.subtask = self.subtaskBook.get_subtask(self, 'Pick')
                found_object = self.object_array.pop()
                # TODO: bug nae norn
                obj_pose = PoseStamped()
                obj_pose.header = found_object.header
                obj_pose.pose.position = found_object.centriod
                self.subtask.pick_object(obj_pose, found_object.name)
                rospy.loginfo('Picking ' + str(found_object.name))
                self.change_state('pick_object')
            else:
                self.change_state('finish')

