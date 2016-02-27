import rospy
from include.abstract_subtask import AbstractSubtask
from std_msgs.msg import Float64

__author__ = 'CinDy'


class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.input_object_pos = None
        self.side_arm = 'right_arm'
        self.subtask = None
        self.check = None
        self.neck = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('pick subtask init')
            # self.neck.tilt = -0.3
            # self.neck.pan = 0
            self.neck = self.skillBook.get_skill(self, 'TurnNeck')
            self.neck.turn(-0.4, 0)
            self.change_state('setting_arm')

        elif self.state is 'setting_arm':
            self.skill = self.skillBook.get_skill(self, 'Pick')
            self.skill.pick_object(self.side_arm)
            self.change_state('detect_object')

        elif self.state is 'detect_object':
            if self.skill.state is 'checking':
                self.check = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
                self.check.start()
                self.change_state('after_detect')

        elif self.state is 'after_detect':
            if self.check.state == 'finish':
                if len(self.check.objects) > 0:
                    self.skill.set_object_pos(self.check.objects[0].point.x,
                                              self.check.objects[0].point.y,
                                              self.check.objects[0].point.z)
                    self.skill.after_mani()
                    self.change_state('grasp_object')

        elif self.state is 'grasp_object':
            print self.skill.state
            if self.skill.state is 'succeed':
                self.change_state('finish')

    def pick_object(self, side):
        rospy.loginfo('------in pick_object:subtask------')
        self.side_arm = side
        self.change_state('init')
