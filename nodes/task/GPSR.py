import rospy
from include.abstract_task import AbstractTask
from include.command_extractor import CommandExtractor
from include.delay import Delay
import utility
from math import atan, sqrt
import tf

__author__ = 'nicole'


class GPSR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.command_extractor = CommandExtractor()
        self.tf_listener = tf.TransformListener()
        self.timer = Delay()
        self.command = None
        self.pick = None
        self.person_pos = None

    def perform(self, perception_data):
        print self.state

        #rospy.loginfo('state in: ' + self.state + ' from: ' + str(perception_data.device) +
        #' data: ' + str(perception_data.input))
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
            self.subtask.turn_absolute(-0.8, 0)

            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            # self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
            # self.subtask = self.subtask.set_position(2, 0, -1.7)
            self.time = Delay()
            self.time.wait(10)
            # self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('pre_start')
            # self.change_state('move_to_start')

        if not perception_data.device in ['DOOR', 'VOICE']:
            return

        if self.state == 'pre_start':
            if not self.time.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask = self.subtask.set_position(3, 1, -1.7)
                self.time = Delay()
                self.time.wait(10)
                self.change_state('move_to_start')

        elif self.state is 'move_pass_door':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('gpsr_start')  # not have yet
                self.change_state('tell_to_commander')

        elif self.state is 'tell_to_commander':
            if self.subtask.state == 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I am in position. If you want to call me. Please wave your hand.')
                self.timer.wait(5)
                self.change_state('wait_for_waving')

        elif self.state is 'wait_for_waving':
            if self.subtask is 'finish' or not self.timer.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'SearchWavingPeople')
                self.change_state('searching_commander')

        elif self.state == 'searching_commander':
            if self.subtask.state is 'finish':
                rospy.loginfo('---searching_commander---')
                self.person_pos = self.tf_listener.transformPoint('map', self.subtask.waving_people_point)
                print "person pos = " + str(self.person_pos)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                size = sqrt(self.person_pos.point.x**2 + self.person_pos.point.y**2)
                self.person_pos.point.x = self.person_pos.point.x/size*(size-0.6)
                self.person_pos.point.y = self.person_pos.point.y/size*size
                self.person_pos.point.z = atan(self.person_pos.point.y/self.person_pos.point.x)
                self.subtask.set_position(self.person_pos.point.x, self.person_pos.point.y,
                                          self.person_pos.point.z)
                self.change_state('move_to_commander')

        elif self.state == 'move_to_commander':
            if perception_data.device is self.Devices.BASE_STATUS:
                rospy.loginfo('---move_to_person---')
                print '---- *****'+str(perception_data.input)
            if self.subtask.state is 'error':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I\'m sorry. I can\'t walk any closer to you. Please wave your hand again.')
                self.timer.wait(5)
                self.change_state('wait_for_waving')
            elif self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I reached you.')
                self.timer.wait(5)
                self.change_state('move_to_start')

        elif self.state is 'move_to_start' and not self.time.is_waiting():
            # if self.subtask.state is 'finish' or not self.timer.is_waiting():
            self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
            self.subtask.turn_absolute(0, 0)
            self.subtask = self.subtaskBook.get_subtask(self, 'Introduce')
            self.change_state('introduce')

        elif self.state is 'introduce':
            if self.subtask.state is 'finish':
                # self.say.state = 'finish'
                # self.voice_mode = self.subtaskBook.get_subtask(self, 'VoiceRecognitionMode')
                # self.voice_mode.recognize(7)
                self.change_state('wait_for_command')

        elif self.state == 'wait_for_command':
            # self.subtask = self.subtaskBook.get_subtask(self, 'ExtractCommand')  # wait for frank
            if perception_data.device is 'VOICE':
                self.command = self.command_extractor.getActions(perception_data.input)
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say(self.command_extractor.make_question(self.command) + ' Please say robot yes or robot no.')
                rospy.loginfo(perception_data.input)
                # self.voice_mode = self.subtaskBook.get_subtask(self, 'VoiceRecognitionMode')
                # self.voice_mode.recognize(6)
                self.timer.wait(7)
                self.change_state('confirm')

        elif self.state == 'confirm':
            if self.say.state == 'finish' or not self.timer.is_waiting():
                if perception_data.device is 'VOICE':
                    if 'robot yes' in perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('OK, I will do it.')
                        self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
                        self.subtask.turn_absolute(-0.8, 0)
                        self.change_state('action')

                    elif 'robot no' in perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('Sorry, Please say again.')
                        # self.voice_mode = self.subtaskBook.get_subtask(self, 'VoiceRecognitionMode')
                        # self.voice_mode.recognize(7)
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
            if len(self.command) > 0:
                goal = self.command[0]
                # print goal, '-------'
                if goal.action == 'go':
                    self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                    location = None
                    if goal.object == "living":
                        location = "living room"
                    elif goal.object == 'dining':
                        location = "dining room"
                    else:
                        location = goal.data
                    self.subtask.to_location(location)
                    self.change_state('moving')
                    self.command.pop(0)
                elif goal.action == 'find' and (goal.object == 'waving person' or goal.object == 'calling person'):
                    self.subtask = self.subtaskBook.get_subtask(self, 'SearchWavingPeople')
                    self.change_state('searching_person')
                    self.command.pop(0)
                elif goal.action == 'grasp':
                    self.pick = self.subtaskBook.get_subtask(self, 'Pick')
                    self.pick.side_arm = 'right_arm'
                    self.change_state('wait_for_arm_init')
                    self.command.pop(0)
                elif goal.action == 'tell' or goal.action == 'say':
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    if goal.object in ['something about yourself']:
                        self.say.say(utility.tell_my_name())
                        self.change_state('action')
                    elif goal.object == "your team's name":
                        self.say.say("My team name is skuba.")
                        self.change_state('action')
                    elif goal.object == "your team's country":
                        self.say.say("I come from thailand")
                        self.change_state('action')
                    elif goal.object == "your team's country":
                        self.say.say("I come from thailand")
                        self.change_state('action')
                    elif goal.object in ['the time', 'what time is it']:
                        self.say.say(utility.tell_the_time())
                        self.change_state('action')
                    elif goal.object == 'what day is today':
                        self.say.say(utility.tell_the_date_today())
                        self.change_state('action')
                    elif goal.object == 'what day is tomorrow':
                        self.say.say(utility.tell_day_tomorrow())
                        self.change_state('action')
                    elif goal.object == 'the day of the month':
                        self.say.say(utility.tell_the_day_of_the_month())
                        self.change_state('action')
                    elif goal.object == 'the day of the week':
                        self.say.say(utility.tell_the_day_of_the_week())
                        self.change_state('action')
                    elif goal.object == "your team's affiliation":
                        self.say.say(utility.tell_affiliation())
                        self.change_state('action')
                    elif goal.object == 'a joke':
                        self.say.say("LA La La La La")
                        self.change_state('action')
                        self.command.pop(0)
                elif goal.action == 'follow':
                    self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                    self.change_state('wait_for_command_follow')
                    self.command.pop(0)

                elif goal.action == 'answer':
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.change_state("wait_for_answer")
                    self.say.say('Please ask me the question.')
                    self.timer.wait(4)
                    # self.voice_mode.recognize(8)
                    self.command.pop(0)
            else:
                self.change_state('finish')

        elif self.state == 'searching_person':
            if self.subtask.state is 'finish':
                rospy.loginfo('---searching_granny---')
                self.person_pos = self.tf_listener.transformPoint('map', self.subtask.waving_people_point)
                print "person pos = " + str(self.person_pos)
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                size = sqrt(self.person_pos.point.x**2 + self.person_pos.point.y**2)
                self.person_pos.point.x = self.person_pos.point.x/size*(size-0.5)
                self.person_pos.point.y = self.person_pos.point.y/size*size
                self.person_pos.point.z = atan(self.person_pos.point.y/self.person_pos.point.x)
                self.subtask.set_position(self.person_pos.point.x, self.person_pos.point.y,
                                          self.person_pos.point.z)
                self.change_state('move_to_person')

        elif self.state == 'move_to_person':
            if perception_data.device is self.Devices.BASE_STATUS:
                rospy.loginfo('---move_to_person---')
                print '---- *****'+str(perception_data.input)
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            if self.subtask.state is 'error':
                self.subtask.say('I\'m sorry. I can\'t walk any closer to you.')
                self.change_state('action')
            elif self.subtask.state is 'finish':
                self.subtask.say('I reached you.')
                self.change_state('action')

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

        elif self.state is 'wait_for_answer':
            if not self.timer.is_waiting():
                if perception_data.device is self.Devices.VOICE:
                    if 'where are you from' == perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('I come from Thailand.')
                        self.change_state('action')
                    elif 'what is your name' == perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('My name is Lumyai.')
                        self.change_state('action')
                    elif 'how is the weather today' == perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say(utility.tell_the_weather_today())
                        self.change_state('action')
                    elif 'what is the date today' == perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say(utility.tell_the_date_today())
                        self.change_state('action')
                    elif 'what day is today' == perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say(utility.tell_day_today())
                        self.change_state('action')
                    elif 'where are we' == perception_data.input:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say(utility.tell_where_are_we())
                        self.change_state('action')

