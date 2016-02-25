__author__ = 'nicole'
import rospy
import subprocess
from include.abstract_task import AbstractTask


class RoboNurse(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.shelf_pos = None
        self.granny_pos = None
        self.pill_dic = {}
        self.pill_name = None
        self.pill_pos = None

    def perform(self, perception_data):
        # if self.state is 'init':
        #     rospy.loginfo('RoboNurse init')
        #     self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
        #     self.subtask.to_location('hallway table')
        #     self.change_state('move_to_hallway')
        #
        # elif self.state is 'move_to_hallway':
        if self.state is 'init':
            # if self.subtask.state is 'finish':
            self.speak('I am in position granny. If you want to call me. Please wave your hand.')
            self.subtask = self.subtaskBook.get_subtask(self, 'DetectWavingPeople')
            self.subtask.start()
            self.change_state('detecting_for_granny')

        elif self.state is 'detecting_for_granny':
            if self.subtask.state is 'finish':
                self.granny_pos = self.subtask.get_point()
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.granny_pos.x, self.granny_pos.y, self.granny_pos.z)
                self.change_state('move_to_granny')

        elif self.state is 'move_to_granny':
            if self.subtask.state is 'error':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I\'m sorry granny. I can\'t walk any closer to you.')
                self.change_state('tell_granny_to_ask_for_pill')
            elif self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I reach you granny.')
                self.change_state('tell_granny_to_ask_for_pill')

        elif self.state is 'tell_granny_to_ask_for_pill':
            if self.subtask.state is 'finish':
                self.subtask.say('If you want me to give you a pill. Say. Robot give me pill.')
                self.change_state('wait_for_granny_command')

        elif self.state is 'wait_for_granny_command':
            if perception_data.device is 'VOICE':
                print perception_data.input == 'robot give me pill'
                if 'pill' in perception_data.input:
                    # self.subtask.say('I am sorry for that granny.' +
                    #                  ' But my hands are not in good condition. ' +
                    #                  'So I can\'t give you a pill. Bye bye')
                    self.subtask.say('Okay, granny.')
                    self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                    self.subtask.set_position(self.shelf_pos.x, self.shelf_pos.y, self.shelf_pos.z)
                    self.change_state('move_to_shelf')

        elif self.state is 'move_to_shelf':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'PillsDetection')
                self.subtask.start()
                self.change_state('collect_pills')

        elif self.state is 'collect_pills':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.granny_pos.x, self.granny_pos.y, self.granny_pos.z)
                self.change_state('take_pill_order')

        elif self.state is 'take_pill_order':
            if self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('Granny.I\'m ready to take an order.')
                if perception_data.device is self.Devices.VOICE :
                    for pill in self.pill_dic:
                        if pill in perception_data.input:
                            self.pill_name = pill
                            self.change_state('move_to_pill')

        elif self.state is 'move_to_pill':
            self.subtask.set_position(self.pill_dic[self.pill_name].x-1.3,
                                      self.pill_dic[self.pill_name].y, self.pill_dic[self.pill_name].z)
            self.change_state('pick_pill')

        elif self.state is 'pick_pill':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Pick')
                self.subtask.pick_object(self, 'right_arm')
                self.change_state('prepare_give_pill')

        elif self.state is 'prepare_give_pill':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.granny_pos.x, self.granny_pos.y, self.granny_pos.z)
                self.change_state('give_pill')

        elif self.state is 'give_pill':
            if self.subtask.state is 'finish':
                self.controlModule.gripper.gripper_open()
                self.controlModule.gripper.gripper_close()
                self.change_state('prepare_leave_arena')

        elif self.state is 'prepare_leave_arena':
            rospy.loginfo('leave arena')
            self.subtask = self.subtaskBook.get_subtask(self, 'LeaveArena')
            self.change_state('leave_arena')

        elif self.state is 'leave_arena':
            if self.subtask.state is 'finish':
                self.change_state('finish')

    def speak(self, message):
        rospy.loginfo("Robot HACKED speak: " + message)
        self.process = subprocess.Popen(["espeak", "-ven+f4", message, "-s 120"])