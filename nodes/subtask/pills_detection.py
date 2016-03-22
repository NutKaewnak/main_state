import tf
from include.transform_point import transform_point
from math import sqrt, pow
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask

__author__ = 'CinDy'


class PillsDetection(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
        self.timer = Delay()
        self.limit_left = 0.3  # pan
        self.limit_right = -0.3
        self.limit_up = 0  # tilt
        self.limit_down = -0.5
        self.new_pan_point = -0.2
        self.new_tilt_point = -0.12

        self.tf_listener = tf.TransformListener()
        self.detect_objects = None
        self.pill_pos = None
        self.pill_name = None
        self.pills_dic = {}
        self.speak = None
        # self.shelf_height = None
        self.tilt_neck = None
        self.count = 0
        self.rem_id = 0
        self.is_performing = False

    def start(self):
        # self.shelf_height = 60
        self.tilt_neck = -0.3
        self.change_state('set_neck')

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True

        if self.state is 'set_neck':
            print '---set_neck---'
            # set neck to left most shelf
            self.turn_neck.turn(self.tilt_neck, self.limit_left)
            # self.timer.wait(2)
            self.change_state('detecting')

        elif self.state is 'detecting':
        # elif self.state is 'detecting' and not self.timer.is_waiting():
        #     print '---detecting---'
            if self.turn_neck.state is 'succeeded':
                if perception_data.device is 'NECK':
                    pan = perception_data.input.pan
                    tilt = perception_data.input.tilt
                    print('pan =' + str(pan))
                    print('tilt =' + str(tilt))
                self.detect_objects = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
                self.detect_objects.start()
                print('--detecting_pill--')
                self.change_state('get_data')

        elif self.state is 'get_data':
            # print 'get_data'
            # self.speak = self.subtaskBook.get_subtask(self, 'Say')
            if self.detect_objects.state is 'finish':
                print 'get_data:found'
                print 'object = ' + str(self.detect_objects.objects)
                # self.pill_pos = []
                # self.pill_pos = self.detect_objects.object_pos.point
                # self.pill_name = 'bottle number ' + str(self.count)
                # self.pills_dic[self.pill_name] = self.pill_pos
                self.change_state('collect_data')

                # print '*********len', len(self.detect_objects.objects)
                # for i in range(len(self.detect_objects.objects)):
                #     obj_goal = transform_point(self.tf_listener, self.detect_objects.objects[i], "map")
                #     pill_width = round(self.detect_objects.objects[i].width.data, 2)
                #     pill_depth = round(self.detect_objects.objects[i].depth.data, 2)
                #     pill_height = round(self.detect_objects.objects[i].height.data, 2)
                #     obj_goal.x = round(obj_goal.x, 5)
                #     obj_goal.y = round(obj_goal.y, 5)
                #     obj_goal.z = round(obj_goal.z, 5)
                #
                #     print 'obj_goal = ', obj_goal
                #     if not self.pills_dic:
                #         self.count += 1
                #         if self.count is 1:
                #             self.pill_name = 'bottle number ' + str(self.count)
                #             self.pills_dic[self.pill_name] = {'width': pill_width, 'height': pill_height,
                #                                           'depth': pill_depth, 'x': obj_goal.x, 'y': obj_goal.y,
                #                                           'z': obj_goal.z}
                #     elif self.pills_dic:
                #         for it in self.pills_dic:
                #             print 'it =', it
                #             print 'pill_dic =', self.pills_dic
                #             if sqrt(pow(self.pills_dic[it]['x'] - obj_goal.x, 2) +
                #                             pow(self.pills_dic[it]['y'] - obj_goal.y, 2)) > 0.3:
                #                 self.count += 1
                #                 self.pill_name = 'bottle number ' + str(self.count)
                #                 self.pills_dic[self.pill_name] = {'width': pill_width, 'height': pill_height,
                #                                                   'depth': pill_depth, 'x': obj_goal.x,
                #                                                   'y': obj_goal.y, 'z': obj_goal.z}
                # print 'pills = ', self.pills_dic
                # temp = PointStamped()
                # temp.header = self.detect_objects.objects[0].header
                # temp.header.stamp = rospy.Time(0)
                # temp.point = self.detect_objects.objects[0].point
                # self.speak = self.subtaskBook.get_subtask(self, 'Say')
                # self.change_state('turn_neck')
                # self.speak.say('measuring.')
            elif self.detect_objects.state is 'not_found':
                print 'get_data:not_found'
                # self.speak = self.subtaskBook.get_subtask(self, 'Say')
                self.change_state('turn_neck')
                # self.speak.say('measuring.')

        elif self.state is 'collect_data':
            print '*********len', len(self.detect_objects.objects)
            for i in range(len(self.detect_objects.objects)):
                print 'i ', i
                obj_goal = transform_point(self.tf_listener, self.detect_objects.objects[i], "map")
                pill_width = round(self.detect_objects.objects[i].width.data, 2)
                pill_depth = round(self.detect_objects.objects[i].depth.data, 2)
                pill_height = round(self.detect_objects.objects[i].height.data, 2)
                # obj_goal.x = round(obj_goal.x, 5)
                # obj_goal.y = round(obj_goal.y, 5)
                # obj_goal.z = round(obj_goal.z, 5)

                print 'obj_goal = ', obj_goal
                if not self.pills_dic:
                    self.pill_name = 'bottle number ' + str(i)
                    self.pills_dic[self.pill_name] = {'width': pill_width, 'height': pill_height,
                                                      'depth': pill_depth, 'x': obj_goal.x, 'y': obj_goal.y,
                                                      'z': obj_goal.z}
                    self.count = i
                    print 'pill_dic ', self.pills_dic
                elif self.pills_dic:
                    print 'len_pills_dic = ', len(self.pills_dic)
                    while True:
                        chk_len = 1
                        for it in self.pills_dic:
                            print 'it =', it
                            print 'pill_dic[it] =', self.pills_dic[it]
                            chk_len = len(self.pills_dic)
                            if sqrt(pow(self.pills_dic[it]['x'] - obj_goal.x, 2) +
                                    pow(self.pills_dic[it]['y'] - obj_goal.y, 2)) >= 0.17:
                                chk_len -= 1
                            else:
                                break
                        if chk_len is 0:
                            self.count = len(self.pills_dic)
                            self.pill_name = 'bottle number ' + str(self.count)
                            self.pills_dic[self.pill_name] = {'width': pill_width, 'height': pill_height,
                                                              'depth': pill_depth, 'x': obj_goal.x,
                                                              'y': obj_goal.y, 'z': obj_goal.z}
                        print 'pills_dic = ', self.pills_dic
                        break
            self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            # if self.speak.state is 'finish':
            # turn left to right
            print '---turn_neck----'
            if perception_data.device is 'NECK':
                pan = perception_data.input.pan
                if pan is None:
                    pan = 0
                print 'pan = ' + str(pan)
                if pan >= self.limit_right:
                    # add +y turn range
                    if pan + self.new_pan_point < self.limit_right:
                        self.new_pan_point = self.limit_right - pan
                    print 'new_pan_point = ' + str(self.new_pan_point)
                    self.turn_neck.turn_relative(0, self.new_pan_point)
                    self.timer.wait(1)
                    self.change_state('detecting')
                else:
                    self.change_state('speak')

        elif self.state is 'speak':
            name = 'bottle number '
            for i in range(self.rem_id, len(self.pills_dic)):
                self.speak.say(name + str(i+1) + 'has width ' + self.pills_dic[name + str(i+1)]['width'] + '.' +
                               ' height ' + self.pills_dic[name + str(i+1)]['height'] + '.' + ' depth ' +
                               self.pills_dic[name + str(i+1)]['depth'] + '.')
                self.timer.wait(3)
                self.is_waiting()
            self.rem_id = len(self.pills_dic)

        elif self.state is 'get_next_line':
            # add +z
            print '---get_next_line---'
            if perception_data.device is 'NECK':
                tilt = perception_data.input.tilt
                if tilt is None:
                    tilt = 0
                print 'tilt = ' + str(tilt)
                # self.tilt_neck -= 0.1225
                if tilt >= self.limit_down:
                    if tilt + self.new_tilt_point < self.limit_down:
                        self.tilt_neck = self.limit_down
                    else:
                        self.tilt_neck = tilt + self.new_tilt_point
                    self.change_state('set_neck')
                else:
                    print 'pills_dic = ', self.pills_dic
                    self.change_state('finish')

        self.is_performing = False

    def is_waiting(self):
        if not self.timer.is_waiting():
            return True
