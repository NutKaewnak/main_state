import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay
from clothing_type_classification.msg import FindClothesResult


__author__ = 'nicole'


class SeparateClothesOP(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.timer = Delay()
        self.cloth_result = None
        self.cloth_result_string = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-1, 0)
            # TODO: static pose not implemented
            self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
            self.subtask.static_pose('Move_aside')
            self.timer.wait(4)
            self.change_state('find_clothes')

        elif self.state is 'find_clothes':
            if not self.timer.is_waiting() or self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask('self', 'FindCloth')
                self.subtask.get_start()
                self.change_state('save_point_from_subtask')

        elif self.state is 'save_point_from_subtask':
            if self.subtask.state is 'finish':
                self.cloth_result = self.subtask.detected_clothes
                self.cloth_result_string = self.subtask.get_description_string()
                rospy.loginfo(self.cloth_result_string)
                self.change_state('say_detail')
            if self.subtask.state is 'not_found':
                self.cloth_result_string = self.subtask.get_description_string()
                rospy.loginfo(self.cloth_result_string)
                self.change_state('find_clothes')

        elif self.state is 'say_detail':
            self.subtask = self.subtask.get_subtask(self, 'Say')
            self.subtask.say(self.cloth_result_string)
            self.timer.wait(15)
            self.change_state('prepare_pick')

        elif self.state is 'prepare_pick':
            self.subtask = self.subtaskBook.get_subtask(self, 'Pick')
            if self.cloth_result:
                self.change_state('pick_cloth')
            else:
                self.change_state('goodbye')

        elif self.state is 'pick_cloth':
            self.subtask.pick_object(self.cloth_result.pop().centroid)
            self.change_state('wait_pick_object')

        elif self.state is 'wait_pick_object':
            if self.subtask.state is 'finish':
                self.subtask.open_gripper()
                self.change_state('prepare_pick')
            elif self.subtask.state is 'unreachable':
                self.change_state('prepare_pick')

        elif self.state is 'goodbye':
            self.subtaskBook.get_subtask(self, 'Say').say('There are no more cloth left for me to pick. Goodbye.')
            # Don't forget to create launch file
