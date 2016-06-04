import rospy
import subprocess
from random import randint
import tf
from include.abstract_task import AbstractTask
from math import atan, sqrt, pi
from include.delay import Delay
from geometry_msgs.msg import PointStamped

__author__ = 'CinDy'


class TestDetectObject(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        # self.shelf_pos =
        self.timer = Delay()
        self.granny_pos = None
        self.pill_dic = {}
        self.pill_name = None
        self.pill_pos = None
        self.pill_data = []
        self.pick = None
        self.point = None
        self.reg_voice = None
        self.tf_listener = tf.TransformListener()
        self.object_pos = None
        self.chk_shelf_pos = False
        self.is_performing = False

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
            self.subtask.start()
            self.change_state('pick_pill')

        elif self.state is 'pick_pill':
            if self.subtask.state is 'finish':
                for goal in self.subtask.objects:
                    # goal = self.tf_listener.transformPoint('map', goal)
                    self.point = goal.point
                    # print self.point, "*******"
                self.pick = self.subtaskBook.get_subtask(self, 'Pick')
                self.state = "wait"

        elif self.state == "wait" and self.pick.state == "wait_for_point":
            self.pick.pick_object(self.point)
            self.change_state('prepare_give_pill')

        elif self.state is 'give_pill':
            if self.subtask.state is 'finish':
                # self.Delay.wait(4)
                # self.pick.gripper_open()
                self.change_state('finish')

        self.is_performing = False


class Pill:
    def __init__(self, width, height, depth, point):
        self.width = width
        self.height = height
        self.depth = depth
        self.point = point
