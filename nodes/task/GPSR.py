__author__ = 'nicole'
import rospy
from include.abstract_task import AbstractTask
from include.command_extractor import CommandExtractor
import utility


class GPSR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.command_extractor = CommandExtractor()
        self.command = None
        self.pick = None
        self.say = self.subtaskBook.get_subtask(self, 'Say')

    def perform(self, perception_data):
        #rospy.loginfo('state in: ' + self.state + ' from: ' + str(perception_data.device) +
                      #' data: ' + str(perception_data.input))
        if self.state is 'init':
            #self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('move_to_start')

        elif self.state is 'move_pass_door':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('gpsr_start')  # not have yet
                self.change_state('move_to_start')

        elif self.state is 'move_to_start':
            if self.subtask == None:
                self.subtask = self.subtaskBook.get_subtask(self, 'Introduce')
                self.change_state('introduce')

        elif self.state is 'introduce':
            if self.subtask.state is 'finish':
                self.say.state = 'finish'
                self.change_state('wait_for_command')

        elif self.state == 'wait_for_command':
            # self.subtask = self.subtaskBook.get_subtask(self, 'ExtractCommand')  # wait for frank
            if self.say.state == 'finish' and perception_data.device is 'VOICE':
                self.command = self.command_extractor.getActions(perception_data.input)
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say(self.command_extractor.make_question(self.command) + ' Please say robot yes or robot no.')
                rospy.loginfo(perception_data.input)
                self.change_state('confirm')

        elif self.state == 'confirm':
            if self.say.state == 'finish' and perception_data.device is 'VOICE':
                if 'robot yes' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('OK, I will do it.')
                    self.change_state('action')
                elif 'robot no' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Sorry, Please say again.')
                    self.change_state('wait_for_command')

        # elif self.state == 'action_1':
        #     if self.say.state == 'finish':
        #         self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
        #         if self.command[0].object is not None:
        #             self.subtask.to_location(self.command[0].data)
        #             self.change_state('finish')
        #         elif self.command[1].object is not None:
        #             self.subtask.to_location(self.command[1].data)
        #             self.change_state('finish')
        elif self.state == 'action':
            if self.say.state == 'finish':
                if len(self.command) > 0:
                    goal = self.command[0]
                    if goal.action == 'go':
                        self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                        self.subtask.to_location(goal.data)
                        self.command.pop(0)
                        self.change_state('moving')
                    elif goal.action == 'grasp':
                        self.pick = self.subtaskBook.get_subtask(self, 'Pick')
                        self.pick.side_arm = 'right_arm'
                        self.change_state('wait_for_arm_init')
                    elif goal.action == 'tell':
                        if goal.object in ['your name', 'the name of your team']:
                            self.say.say(utility.tell_my_name())
                            self.change_state('action')
                        elif goal.object in ['the time', 'what time is it']:
                            self.say.say(utility.tell_the_time())
                            self.change_state('action')
                        elif goal.object == 'the date today':
                            self.say.say(utility.tell_the_date_today())
                            self.change_state('action')
                        elif goal.object == 'the date tomorrow':
                            self.say.say(utility.tell_day_tomorrow())
                            self.change_state('action')
                        elif goal.object == 'the day of the month':
                            self.say.say(utility.tell_the_day_of_the_month())
                            self.change_state('action')
                        elif goal.object == 'the day of the week':
                            self.say.say(utility.tell_the_day_of_the_week())
                            self.change_state('action')
                        elif goal.object == 'affiliation':
                            self.say.say(utility.tell_affiliation())
                            self.change_state('action')
                    elif goal.action == 'follow':
                        self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                        self.change_state('wait_for_command_follow')
                else:
                    self.change_state('finish')

        elif self.state == 'moving':
            if self.subtask.state == 'finish':
                self.change_state('action')

        elif self.state is 'wait_for_arm_init':
            if self.pick.state is 'wait_for_point':
                rospy.loginfo('---in test---')
                self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
                self.subtask.turn_absolute(-0.4, 0.0)
                self.change_state('wait_for_turn_neck')

        elif self.state is 'wait_for_turn_neck':
            if self.subtask.state is 'finish':
                self.change_state('find_object')

        elif self.state is 'find_object':
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
            self.subtask.start()
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            if self.subtask.state is 'finish':
                self.object_goal = self.subtask.objects[0].point
                self.change_state('pick')

        elif self.state is 'pick':
            self.current_subtask = self.pick
            self.pick.pick_object(self.object_goal)
            self.change_state('wait_for_pick')

        elif self.state is 'wait_for_pick':
            if self.pick.state is 'finish':
                self.change_state('action')

        elif self.state is 'wait_for_command_follow':
            if perception_data.device is self.Devices.VOICE and 'follow me' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                self.follow = self.subtaskBook.get_subtask(self, 'FollowMe')
                self.change_state('follow_init')

        elif self.state is 'follow_init':
            self.follow.start()
            self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if perception_data.device is self.Devices.VOICE and 'stop' in perception_data.input:
                self.change_state('wait_for_command_follow')