from include.abstract_subtask import AbstractSubtask
__author__ = 'Nicole'


class DetectBlanket(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.blanket_pos = None
        self.new_neck_point = None
        self.neck_direction = 'right'
        self.limit_down = 0.8
        self.limit_up = -0.8

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.skill.turn(0, 0)
            # self.subtask = self.subtaskBook.get_subtask(self, '')
            # self.timer.wait(3)
            self.change_state('searching')

        elif self.state is 'searching':
            print('skill_in_search = ' + self.skill.state)
            if self.skill.state is 'succeeded':
                print '---searching---'
                print 'state = ' + self.state
                # self.subtask.start()
                self.change_state('detecting')

        elif self.state is 'detecting':
            # if self.subtask.state is 'finish':
            #     print 'find phone'
            #     self.blanket_pos = self.subtask.get_point()
                self.change_state('finish')
            # elif self.subtask.state is 'not_found':
            #     print 'can\'t find phone'
            #     self.change_state('prepare_to_turn_neck')

        elif self.state is 'prepare_to_turn_neck':
            if perception_data.device is 'NECK':
                pan = perception_data.input.pan
                if pan is None:
                    pan = 0
                print 'pan =' + str(pan)
                if self.neck_direction is 'right':
                    if pan + 0.3 <= self.limit_up:
                        self.new_neck_point = 0.3
                        print 'new_neck =' + str(self.new_neck_point)

                    else:
                        self.new_neck_point = self.limit_up - pan
                        self.neck_direction = 'left'
                else:
                    if pan - 0.3 >= self.limit_down:
                        self.new_neck_point = -0.3
                    else:
                        self.new_neck_point = self.limit_down + pan
                        self.neck_direction = 'right'
                self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            self.skill.turn_relative(0, self.new_neck_point)
            print('----turn_neck----')
            # self.timer.wait(3)
            self.change_state('searching')

# Don't forget to add this subtask to subtask book