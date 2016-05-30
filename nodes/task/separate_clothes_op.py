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
        self.right_side = None
        self.cloth_result = None
        self.cloth_result_string = None
        self.is_performing = False

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True

        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.6, -0.1)
            self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
            self.subtask.static_pose('right_picking_before_prepare_1')
            self.timer.wait(4)
            self.change_state('find_clothes')

        elif self.state is 'find_clothes':
            if not self.timer.is_waiting() or self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'FindCloth')
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
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say(self.cloth_result_string)
            self.timer.wait(15)
            self.change_state('prepare_pick')

        elif self.state is 'prepare_pick':
            if self.subtask.state is 'finish' or not self.timer.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'Pick')
                if self.cloth_result:
                    self.change_state('pick_cloth')
                else:
                    self.change_state('goodbye')

        elif self.state is 'pick_cloth':
            cloth = self.cloth_result.pop()
            self.subtask.pick_object(cloth.centroid)
            self.right_side = cloth.color == 2
            self.change_state('wait_pick_object')
            self.timer.wait(20)

        elif self.state is 'wait_pick_object':
            if self.subtask.state is 'finish':
                self.change_state('turn_side')
            elif self.subtask.state is 'unreachable':
                self.change_state('prepare_pick')
            if not self.timer.is_waiting():
                self.change_state('manual')
                self.timer.wait(60)

        elif self.state is 'turn_side':
            self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
            if self.right_side:
                self.subtask.static_pose('turn_arm_right')
            else:
                self.subtask.static_pose('turn_arm_left')
            self.timer.wait(5)

        elif self.state is 'wait_turn_side':
            if self.subtask.state is 'finish' or not self.timer.is_waiting():
                self.subtask.open_gripper()
                self.change_state('prepare_pick')
                self.right_side = None

        elif self.state is 'manual':
            # self.testByInvk.TestInvKine()
            if self.timer.is_waiting():
                self.change_state('goodbye')

        elif self.state is 'goodbye':
            self.subtaskBook.get_subtask(self, 'Say').say('There are no more cloth left for me to pick. Goodbye.')
            self.change_state('exit')

        self.is_performing = False
