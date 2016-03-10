import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'CinDy'


class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.input_object_point = None
        self.side_arm = None
        self.subtask = None
        self.neck = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('pick subtask init')
            self.skill = self.skillBook.get_skill(self, 'Grasp')
            self.skill.set_side(self.side_arm)
            self.change_state('wait_for_skill_init')

        elif self.state is 'wait_for_skill_init':
            if self.skill.state is 'wait_for_point':
                self.change_state('wait_for_point')

        elif self.state is 'receive_point':
            print 'kuy kuy kuy'
            self.change_state('setting_arm')

        elif self.state is 'setting_arm':
            self.skill.pick_object(self.input_object_point)
            self.change_state('wait_for_skill')

        elif self.state is 'wait_for_skill':
            if self.skill.state is 'done_prepare':
                self.skill.after_prepare()
            elif self.skill.state is 'unreachable':
                self.change_state('solve_unreachable')
            elif self.skill.state is 'succeed':
                self.change_state('finish')

    def pick_object(self, point):
        """
        Let subtask pick object. Please make sure that side arm is already design (Default: 'right_arm').
        :param point: (Point) point of object to pick.
        :return: None
        """
        self.input_object_point = point
        if self.side_arm is None:
            self.side_arm = 'right_arm'
        self.change_state('receive_point')

    def open_gripper(self):
        self.skillBook.get_skill(self, 'Graps').open_gripper()

    def close_gripper(self):
        self.skill = self.skillBook.get_skill(self, 'Graps').close_gripper()
