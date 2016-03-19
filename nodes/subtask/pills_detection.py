import rospy
import tf
from geometry_msgs.msg import PointStamped
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask

__author__ = 'CinDy'


class PillsDetection(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
        self.timer = Delay()
        self.limit_left = 0.4  # pan
        self.limit_right = -0.4
        self.limit_up = 0      # tilt
        self.limit_down = 0
        self.new_neck_point = 0.3
        self.neck_direction = 'right'

        self.tf_listener = tf.TransformListener()
        self.detect_objects = None
        self.pill_pos = None
        self.pill_name = None
        self.pill_width = None
        self.pill_height = None
        self.pill_depth = None
        self.pills_dic = {}
        self.speak = None
        self.turn_range = None
        self.shelf_height = None
        # self.tilt_neck = None
        # self.pan_neck = None
        self.count = 0

    def start(self):
        self.shelf_height = 60
        self.tilt_neck = 0
        self.pan_neck = -0.34
        self.change_state('set_neck')

    def perform(self, perception_data):
        if self.state is 'set_neck':
            # set neck to left most shelf
            self.turn_neck.turn(self.tilt_neck, self.limit_left)
            self.timer.wait(2)
            self.change_state('detecting')

        elif self.state is 'detecting' and not self.timer.is_waiting():
            if self.turn_neck.state is 'succeeded':
                if perception_data.device is 'NECK':
                    pan = perception_data.input.pan
                    tilt = perception_data.input.tilt
                    print('pan =' + str(pan))
                    print('tilt =' + str(tilt))
                # print 'pitch ='+str(self.turn_neck.pitch)
                # print 'pan ='+str(self.turn_neck.pan)
                self.detect_objects = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
                self.detect_objects.start()
                print('--detecting_pill--')
                self.change_state('get_data')

        elif self.state is 'get_data':
            print 'get_data'
            if self.detect_objects.state is 'finish':
                print 'objects = ' + str(self.detect_objects.objects)
                self.pill_pos = self.detect_objects.objects[0].point
                self.pill_width = self.detect_objects.objects[0].width.data
                self.pill_depth = self.detect_objects.objects[0].depth.data
                self.pill_height = self.detect_objects.objects[0].height.data
                self.count += 1
                # self.pill_pos = []
                # temp = PointStamped()
                # temp.header = self.detect_objects.objects.header
                # temp.point = self.detect_objects.objects[0].point
                # self.pill_pos = self.tf_listener.transformPoint('odom', temp)
                # self.pill_name = self.detect_objects.name
                self.pill_name = 'bottle number ' + str(self.count)
                self.pills_dic[self.pill_name] = self.pill_pos
                self.speak = self.subtaskBook.get_subtask(self, 'Say')
                self.speak.say(self.pill_name + ' has width ' + str(self.pill_width) + ' height ' + str(
                    self.pill_height) + ' depth ' + str(self.pill_depth))
                self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            if self.speak.state is 'finish':
                # turn left to right
                print '---turn_neck----'
                if perception_data.device is 'NECK':
                    pan = perception_data.input.pan
                    tilt = perception_data.input.tilt
                    if pan is None:
                        pan = 0
                    if tilt is None:
                        tilt = 0
                    print 'pan = ' + str(pan)
                    print('tilt =' + str(tilt))
                    self.pan_neck += 0.11
                    if self.pan_neck < 0.34:
                        # add +y turn range
                        self.turn_neck.turn_relative(0, 0.11)
                        self.change_state('detecting')
                    else:
                        self.change_state('get_next_line')

        # elif self.state is 'turn_neck':
        #     if self.turn_neck.state is 'succeeded':
        #         if perception_data.device is 'NECK':
        #             pan = perception_data.input.pan
        #             tilt = perception_data.input.tilt
        #             print('pan =' + str(pan))
        #             print('tilt =' + str(tilt))
        #             if pan < 0.34:
        #                 # add +y turn range
        #                 self.change_state('detecting')
        #             else:
        #                 self.change_state('get_next_line')

        elif self.state is 'get_next_line':
            # add +z
            self.tilt_neck -= 0.1225
            if self.tilt_neck > -0.994:
                self.change_state('set_neck')
            else:
                self.change_state('finish')
