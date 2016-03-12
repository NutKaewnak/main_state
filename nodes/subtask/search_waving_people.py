from include.abstract_subtask import AbstractSubtask
from include.delay import Delay
import rospy
__author__ = 'Nicole'


class SearchWavingPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'TurnNeck')
        self.subtask = self.current_subtask
        self.timer = Delay()
        self.limit_up = 0.8  # pan
        self.limit_down = -0.8
        self.neck_direction = 'right'
        self.waving_people_point = None
        self.new_neck_point = 0.3
        self.pan = 0

    def perform(self, perception_data):
        # if perception_data.device is 'NECK':
        #     self.pan = perception_data.input.pan
        print self.state, '&&&&&&&'
        if self.state is 'init':
            # self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.skill.turn(0, 0)
            self.timer.wait(5)
            self.change_state("wait_turn_neck_0_0")

        elif self.state is "wait_turn_neck_0_0" and not self.timer.is_waiting():
            self.change_state('searching')

        elif self.state is 'searching':
            if perception_data.device is 'NECK':
                print('skill_in_search = ' + self.skill.state)
                if not self.skill.is_active:
                    self.change_state('detecting')
                    print '---searching waving---'
                    print 'state = ' + self.state
                    self.subtask = self.subtaskBook.get_subtask(self, 'DetectWavingPeople')
                    self.subtask.start()
                    print 'detectWaving subtask state = ' + self.subtask.state

        elif self.state is 'detecting':
            if self.subtask.state is 'finish':
                print 'find people'
                self.waving_people_point = self.subtask.get_point()
                self.change_state('finish')
            # elif not self.timer.is_waiting():

            elif self.subtask.state is 'not_found':
                print 'can\'t find people'
                self.change_state('prepare_to_turn_neck')

        elif self.state is 'prepare_to_turn_neck':
            if perception_data.device is 'NECK':
                pan = perception_data.input.pan
                if pan is None:
                    pan = 0
                print 'pan = ' + str(pan)
                if self.neck_direction is 'left':
                    if pan + 0.3 <= self.limit_up:
                        self.new_neck_point = 0.3
                    else:
                        self.new_neck_point = self.limit_up - pan
                        self.neck_direction = 'right'
                else:
                    if pan - 0.3 >= self.limit_down:
                        self.new_neck_point = -0.3
                    else:
                        self.new_neck_point = self.limit_down + pan
                        self.neck_direction = 'left'
                print 'new_neck = ' + str(self.new_neck_point)
                self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            print '--turn^^^'
            # rospy.sleep(5000)
            # self.skill.turn_relative(0, self.new_neck_point)
            # rospy.sleep(5000)
            if perception_data.device is 'NECK':
                self.pan = perception_data.input.pan
                # self.skill = self.skillBook.get_skill(self, 'TurnNeck')
                self.skill.turn_relative(0, self.new_neck_point)
                self.timer.wait(5)
                self.change_state("wait_turn_neck_relative")
        elif self.state is "wait_turn_neck_relative" and not self.timer.is_waiting():
            print 'pan =' + str(self.pan)
            print('----turn_neck----')
            self.change_state('searching')
            # self.timer.wait(3)
