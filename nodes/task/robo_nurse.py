import rospy
import subprocess
from random import randint
import tf
from include.abstract_task import AbstractTask
from math import atan, sqrt
from include.delay import Delay
from geometry_msgs.msg import PointStamped

__author__ = 'CinDy'


class RoboNurse(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        # self.shelf_pos =
        self.granny_pos = None
        self.pill_dic = {}
        self.pill_name = None
        self.pill_pos = None
        self.pick = None
        self.reg_voice = None
        self.tf_listener = tf.TransformListener()
        self.object_pos = None
        self.chk_shelf_pos = False

    def perform(self, perception_data):
        # if self.state is 'init':
        #     rospy.loginfo('RoboNurse init')
        #     self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
        #     self.subtask.to_location('hallway table')
        #     self.change_state('move_to_hallway')
        #
        # elif self.state is 'move_to_hallway':
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.change_state('detect_pills')
            # self.change_state('init_detecting')
            rospy.loginfo('---in task---')
            # self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('I am in position granny. If you want to call me. Please wave your hand.')

        elif self.state is 'init_detecting':
            if self.subtask.state is 'finish':
                rospy.loginfo('---init_detecting---')
                self.subtask = self.subtaskBook.get_subtask(self, 'SearchWavingPeople')
                # self.subtask.start()
                self.change_state('searching_granny')

        elif self.state is 'searching_granny':
            # print 'Searching.state =' + self.subtask.state
            if self.subtask.state is 'finish':
                rospy.loginfo('---searching_granny---')
                self.granny_pos = self.tf_listener.transformPoint('map', self.subtask.waving_people_point)
                print "granny pos = " + str(self.granny_pos)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                size = sqrt(self.granny_pos.point.x**2 + self.granny_pos.point.y**2)
                self.subtask.set_position(self.granny_pos.point.x/size*(size-0.5), self.granny_pos.point.y/size*size, atan(self.granny_pos.point.y/self.granny_pos.point.x))
                self.change_state('move_to_granny')

        elif self.state is 'move_to_granny':
            if perception_data.device is self.Devices.BASE_STATUS:
                rospy.loginfo('---move_to_granny---')
                print '---- *****'+str(perception_data.input)
            if self.subtask.state is 'error':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I\'m sorry granny. I can\'t walk any closer to you.')
                self.change_state('tell_granny_to_ask_for_pill')
            elif self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I reached you granny.')
                self.change_state('watch_granny')

        elif self.state is 'watch_granny':
            if self.subtask.state is 'finish':
                rospy.loginfo('---watching granny---')
                self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
                self.subtask.turn_absolute(-0.25, 0)
                self.change_state('tell_granny_to_ask_for_pill')

        elif self.state is 'tell_granny_to_ask_for_pill':
            if self.subtask.state is 'finish':
                rospy.loginfo('---tell_granny_ask_pill---')
                self.change_state('wait_for_granny_command')
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('If you want me to give you a pill. Say. I need my pill.')
                self.reg_voice = self.subtaskBook.get_subtask(self, 'VoiceRecognitionMode')
                self.reg_voice.recognize(4)
                # self.subtaskBook.get_subtask(self, 'VoiceRecognitionMode').recognize(1)

        elif self.state is 'wait_for_granny_command':
            # rospy.loginfo('---wait_for_granny_command---')
            if perception_data.device is self.Devices.VOICE:
                # print 'helloo'
                print perception_data.input
                print perception_data.input == 'robot I need my pill'
                if 'pill' in perception_data.input:
                    self.subtask.say('Okay, granny.')
                    self.change_state('init_move')

        elif self.state is 'init_move':
            print self.state
            # if self.subtask.state is 'finish':
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('shelf')
            self.change_state('move_to_shelf')
            rospy.loginfo('---init_move---')

        elif self.state is 'move_to_shelf':
            print 'state =' + str(self.subtask.state)
            print 'perception_module_base_pos = ' + str(self.perception_module.base_status.position)
            chk_shelf = self.perception_module.base_status.position
            print 'chk = ' + str(chk_shelf)
            #  need to change if setting new position
            if 12.100 <= chk_shelf[0] <= 12.500:
                if -6.000 <= chk_shelf[1] <= -5.600:
                    if 2.600 <= chk_shelf[2] <= 3.000 or -3.300 <= chk_shelf[2] <= -2.700:
                        self.chk_shelf_pos = True
            print 'self.chk_shelf = ' + str(self.chk_shelf_pos)
            if self.subtask.state is 'finish' or self.chk_shelf_pos:
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I saw The leftmost bottle')
                self.change_state('detect_pills')

        elif self.state is 'detect_pills':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'PillsDetection')
                self.subtask.start()
                self.change_state('collect_pills')

        elif self.state is 'collect_pills':
            if self.subtask.state is 'finish':
                rospy.loginfo('---collect_pills---')
                self.pill_dic = self.subtask.pills_dic
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.granny_pos.point.x, self.granny_pos.point.y, self.granny_pos.point.z)
                self.change_state('take_pill_order')

        elif self.state is 'take_pill_order':
            if self.subtask.state is 'finish':
                rospy.loginfo('---take_pill_order---')
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('Granny.I\'m ready to take an order.')
                self.change_state('wait_for_order')

        elif self.state is 'wait_for_order':
            if self.subtask.state is 'finish':
                rospy.loginfo('---wait_for_order---')
                if perception_data.device is self.Devices.VOICE:
                    for pill in self.pill_dic:
                        if pill in perception_data.input:
                            self.pill_name = pill
                            self.change_state('move_to_pill')

        elif self.state is 'move_to_pill':
            print self.pill_dic[self.pill_name]
            size = sqrt(self.pill_dic[self.pill_name].x**2 + self.pill_dic[self.pill_name].y**2)
            self.subtask.set_position(self.pill_dic[self.pill_name].x/size*(size-0.8),
                                      self.pill_dic[self.pill_name].y, self.pill_dic[self.pill_name].z)
            self.change_state('pick_pill')

        elif self.state is 'pick_pill':
            if self.subtask.state is 'finish':
                rospy.loginfo('---pick_pill---')
                # self.pick = self.subtaskBook.get_subtask(self, 'Pick')
                # self.pick.pick_object(self, self.pill_dic[self.pill_name])
                self.change_state('prepare_give_pill')

        elif self.state is 'prepare_give_pill':
            if self.subtask.state is 'finish':
                rospy.loginfo('---prepare_give_pill---')
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.granny_pos.point.x, self.granny_pos.point.y, self.granny_pos.point.z)
                self.change_state('give_pill')

        elif self.state is 'give_pill':
            if self.subtask.state is 'finish':
                self.Delay.wait(4000)
                # self.pick.gripper_open()
                self.change_state('finish')

        elif self.state is 'detecting_granny':
            print 'random subtask'
            rand = randint(0, 2)
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            if rand == 0:
                print 'drop blanket'
                self.subtask.say('Granny you drop blanket.')
                self.change_state('drop_blanket')
            elif rand == 1:
                print 'falling granny'
                self.subtask.say('Help! granny fell')
                self.change_state('falling_granny')
            elif rand == 2:
                print 'granny stands up and walk away + sit'
                self.subtask.say('granny you forgot your cane')
                self.change_state('granny_walk')

        elif self.state is 'drop_blanket':
            if self.subtask.state is 'finish':
                print 'drop blanket'
                self.subtask = self.subtaskBook.get_subtask('DetectBlanket')
                self.change_state('detect_blanket')

        elif self.state is 'falling_granny':
            if self.subtask.state is 'finish':
                print 'find phone'
                self.subtask = self.subtaskBook.get_subtask('DetectPhone')
                self.change_state('detect_phone')

        elif self.state is 'granny_walk':
            if self.subtask.state is 'finish':
                print 'find cane'
                self.subtask = self.subtaskBook.get_subtask('DetectCane')
                self.change_state('detect_cane')

        elif self.state is 'detect_blanket':
            if self.subtask.state is 'finish':
                print 'detect_blanket'
                self.object_pos = [5, 5, 5]
                self.change_state('move_to_object')

        elif self.state is 'detect_phone':
            if self.subtask.state is 'finish':
                print 'detect_phone'
                self.object_pos = [5, 5, 5]
                self.change_state('move_to_object')

        elif self.state is 'detect_cane':
            if self.subtask.state is 'finish':
                print 'detect_cane'
                self.object_pos = [5, 5, 5]
                self.change_state('move_to_object')

        elif self.state is 'move_to_object':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.object_pos[0], self.object_pos[1], self.object_pos[2])
                self.change_state('pick_object')

        elif self.state is 'pick_object':
            if self.subtask.state is 'finish':
                # self.pick.pick_object(self, self.object_pos)
                self.change_state('finish')

        # elif self.state is 'prepare_leave_arena':
        #     rospy.loginfo('leave arena')
        #     self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
        #     self.change_state('leave_arena')
        #
        # elif self.state is 'leave_arena':
        #     if self.subtask.state is 'finish':
        #         self.change_state('finish')

    def speak(self, message):
        rospy.loginfo("Robot HACKED speak: " + message)
        self.process = subprocess.Popen(["espeak", "-ven+f4", message, "-s 120"])
