import rospy
from include.abstract_task import AbstractTask
from include.get_distance import get_distance
from include.delay import Delay
from std_msgs.msg import Float64
from math import hypot
import tf

__author__ = 'Frank'


class RestaurantFrank(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.init_location = None
        self.location_list = {'table one': [], 'table two': [], 'table three': [], 'kitchen': []}
        # self.direction_list = {'location one': [], 'location two': [], 'location three': [], 'kitchen': []}
        self.command = None
        self.count = 0
        self.first = None
        self.waving_people = []
        self.current_table = None
        self.stack_table = None
        self.order = {'table one': [], 'table two': [], 'table three': []}
        self.food = ['choco syrup', 'chips', 'bisquits', 'pretzels', 'baby sweets', 'pringles',
                     'egg', 'beer', 'apple', 'coconut milk', 'paprika', 'coke', 'pumper nickel', 'tea']
        self.say = None
        self.follow = None
        self.move_to = None
        self.move_abs = None
        self.move_relative = None
        self.detect_waving_people = {'table one': False, 'table two': False, 'table three': False}
        self.turn_neck = None
        self.first_table = True
        self.tf_listener = tf.TransformListener()
        self.delay = Delay()
        self.track_id = None
        self.subtask = None

    def perform(self, perception_data):
        print self.state, '***'
        # if self.say.speak.controlModule.speaker.process is not None:
        # print self.say.speak.controlModule.speaker.is_finish(), "++++++++"
        if self.state is 'init':
            self.turn_neck = self.subtaskBook.get_subtask(self, 'TurnNeck')
            self.turn_neck.turn_absolute(0, 0)
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            # print 'subtask state ='+self.subtask.state
            # print 'state =' + self.state
            # if self.subtask.state is 'finish' or not self.timer.is_waiting():
            if perception_data.device is self.Devices.VOICE:
                print 'input = ' + str(perception_data.input)
                if 'follow me' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I will follow you')
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                    self.change_state('follow_init')

        # elif self.state is 'confirm_follow':
        #     if perception_data.device is self.Devices.VOICE:
        #         if perception_data.input == 'robot yes':
        #             self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
        #             self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
        #             self.change_state('follow_init')
        #         elif perception_data.input == 'robot no':
        #             self.subtaskBook.get_subtask(self, 'Say').say('Sorry. Please tell me again.')
        #             self.change_state('wait_for_command')

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE_LEG:
                # print 'hi'
                min_distance = 99
                self.track_id = -1
                for person in perception_data.input.people:
                    print 'person = ', person
                    if (person.pos.x > 0.8 and person.pos.x < 1.8
                        and person.pos.y > -1 and person.pos.y < 1):
                        distance = hypot(person.pos.x, person.pos.y)
                        print 'person id =', person.object_id
                        if distance < min_distance:
                            self.track_id = person.object_id
                if self.track_id != -1:
                    print self.track_id
                    self.follow.set_person_id(self.track_id)
                    self.change_state('follow')

        elif self.state is 'follow':
            print 'state =' + self.state
            # recovery follow
            if perception_data.device is self.Devices.VOICE:
                if 'robot stop' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                    self.track_id = -1
                    if self.location_list['table one'] != [] and self.location_list['table two'] != [] and \
                                    self.location_list['table three'] != []:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('I am at the kitchen bar. Is it on your left or on your right ?')
                        self.change_state('ask_for_kitchen')
                    else:
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('Where is this place ?')
                        self.change_state('ask_for_location')
                elif 'robot waiting' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Wait for command.')
                    self.change_state('wait_for_command')

            if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input.people:
                print 'track_id =', self.track_id
                for person in perception_data.input.people:
                    print ' person.id =', person.object_id
                    if self.track_id == person.object_id:
                        break
                    elif self.follow.guess_id == person.object_id:
                        self.track_id = self.follow.guess_id
                        print 'change track id = ', self.track_id
                    # elif perception_data.input.people[-1]:
                    # elif self.follow.isLost:
                    #     self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    #     self.subtask.say('I am lost tracking. Please wave your hand.')
                    #     self.delay.wait(2)
                    #     self.change_state('detect_waving_people')

        elif self.state is 'ask_for_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location.replace("my", "your")
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say(self.location + '. robot yes or robot no ?')
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                if 'left' in self.location:
                    self.location_list[self.location] = (
                    self.perception_module.base_status.position[0], self.perception_module.base_status.position[1],
                    self.perception_module.base_status.position[2] + 1.57)

                    # self.direction_list[self.location] = 'left'
                else:
                    self.location_list[self.location] = (
                    self.perception_module.base_status.position[0], self.perception_module.base_status.position[1],
                    self.perception_module.base_status.position[2] - 1.57)

                    # self.direction_list[self.location] = 'right'
                print self.location_list
                # print self.direction_list
                self.change_state('init')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

        elif self.state is 'ask_for_kitchen':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                if 'left' in perception_data.input:
                    self.location = 'kitchen bar is on your left'
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say(self.location + '. robot yes or robot no ?')
                    self.change_state('confirm_kitchen')
                elif 'right' in perception_data.input:
                    self.location = 'kitchen bar is on your right'
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say(self.location + '. robot yes or robot no ?')
                    self.change_state('confirm_kitchen')

        elif self.state is 'confirm_kitchen':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                if 'left' in self.location:
                    self.location_list[self.location] = (
                    self.perception_module.base_status.position[0], self.perception_module.base_status.position[1],
                    self.perception_module.base_status.position[2] + 1.57)
                    # self.direction_list[self.location] = 'left'
                else:
                    self.location_list[self.location] = (
                    self.perception_module.base_status.position[0], self.perception_module.base_status.position[1],
                    self.perception_module.base_status.position[2] - 1.57)
                    # self.direction_list[self.location] = 'right'
                print self.location_list
                # print self.direction_list
                self.change_state('talk_to_barman')

            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , Is it on your left or on your right ?')
                self.change_state('ask_for_kitchen')

        elif self.state is 'talk_to_barman':
            if self.say.state is not 'finish':
                return
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.say.say('which table do you want me to go.')
            self.change_state('wait_for_barman_first')

        elif self.state is 'wait_for_barman_first':
            if self.say.state is not 'finish':
                return

            if perception_data.device is self.Devices.VOICE:
                print perception_data.input
                print self.location_list
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = location
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('Do you want me to go ' + self.command + '. robot yes or robot no .')
                        # self.delay.wait(5)
                        self.change_state('confirm_command')

        elif self.state is 'confirm_command':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I will go to ' + self.command + '.')
                self.current_table = self.command
                self.move_abs = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.move_abs.set_position(self.location_list[self.command][0], self.location_list[self.command][1],
                                           self.location_list[self.command][2])
                self.change_state('move_to_location')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , What did you say ?')
                self.change_state('wait_for_barman_first')

        elif self.state is 'move_to_location':
            if self.move_abs.state is 'finish':
                # self.delay.wait(3)
                # self.change_state('wait_for_order')
                # self.change_state('turning_1')
                self.change_state('say_for_order')
            elif self.move_abs.state is 'error':
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                # self.say.say('I cannot walk to the table.')
                self.change_state('say_for_order')

        elif self.state is 'say_for_order':
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.say.say('Hello sir, What order you will take ?')
            self.delay.wait(5)
            self.change_state('wait_for_order')

        elif self.state is 'wait_for_order':
            if self.say.state is not 'finish' or self.delay.is_waiting():
                return
            if perception_data.device is self.Devices.VOICE:
                for food in self.food:
                    if food in perception_data.input:
                        self.order[self.current_table].append(food)
                if not self.order[self.current_table]:
                    return
                else:
                    self.change_state('ask_for_order')
                    # self.say.say('Your orders are ' + " and ".join(self.order[self.current_table]))

        elif self.state is 'ask_for_order':
            self.say.say(
                'Do you want ' + " and ".join(self.order[self.current_table]) + ' . Please say robot yes or robot no.')
            self.delay.wait(7)
            self.change_state('confirm_for_order')

        elif self.state is 'confirm_for_order':
            if self.say.state is not 'finish' or self.delay.is_waiting():
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Ok')
                # if self.first_table == True:
                #     # self.say.say('I will go to ' ted_local_planner_params.yaml+ self.stack_table + ' to get a order.')
                #     self.first_table = False
                self.detect_waving_people[self.current_table] = True
                for i in self.detect_waving_people:
                    if self.detect_waving_people[i] == False:
                        self.command = i
                        self.change_state('move_to_another_table')
                else:
                    self.change_state('move_to_kitchen')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , What did you say ?')
                self.change_state('wait_for_order')

        elif self.state == 'move_to_another_table':
            # self.command = location
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.say.say('I am going to' + self.command + '.')
            self.delay.wait(5)
            self.change_state('confirm_command_auto')

        elif self.state == 'confirm_command_auto':
            if self.say.state is not 'finish' or self.delay.is_waiting():
                return
            self.move_abs = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            self.move_abs.set_position(self.location_list[self.command][0], self.location_list[self.command][1],
                                       self.location_list[self.command][2])
            self.change_state('turning_1_2')

        # elif self.state == 'move_to_location_auto':
        elif self.state is 'turning_1_2':
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.say.say("I am searching for waving person.")

        elif self.state is 'init_detect':
            self.move_relative = self.subtaskBook.get_subtask(self, 'MoveRelative')
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_1_2')

        elif self.state is 'waving_1_2' and not self.delay.is_waiting():
            self.detect_waving_people = self.subtaskBook.get_subtask(self, 'DetectWavingPeople')
            self.detect_waving_people.start()
            self.change_state('wait_for_waving_1_2')

        elif self.state is 'wait_for_waving_1_2':
            if self.detect_waving_people.state is 'not_found':
                self.change_state('init_detect')
            elif self.detect_waving_people.state is 'finish':
                if not self.detect_waving_people.get_point() == None:
                    self.waving_people.append(self.detect_waving_people.get_point())  # !!!!!!
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say("Please waiting. I will go there.")
                    self.move_relative = self.subtaskBook.get_subtask(self, 'MoveRelative')
                    self.move_relative.set_position(self.detect_waving_people.get_point())
                    self.change_state('move_to_location')
                    # self.change_state('init_detect')
                    # self.change_state('decision_for_waving')

        elif self.state is 'decision_for_waving':
            if self.waving_people != []:
                self.change_state('set_to_waving_table')

        elif self.state is 'set_to_waving_table':
            if self.say.state is not 'finish':
                return
            if self.stack_table is not None:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I am going to ' + self.stack_table + ' to get a order.')
                self.move_abs = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.move_abs.set_position(self.location_list[self.stack_table][0],
                                           self.location_list[self.stack_table][1],
                                           self.location_list[self.stack_table][2])
                self.current_table = self.stack_table
                self.change_state('move_to_waving_table')

        elif self.state is 'move_to_waving_table':
            if self.move_abs.state is 'finish':
                self.change_state('say_for_order')

        elif self.state is 'set_to_kitchen':
            # if self.say.state is not 'finish':
            #     return
            # if self.stack_table is not None:
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.say.say('I will go back to kitchen bar .')
            self.move_abs = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            self.move_abs.set_position(self.location_list['kitchen'][0], self.location_list['kitchen'][1],
                                       self.location_list['kitchen'][2])
            self.current_table = self.stack_table
            self.change_state('move_to_kitchen')

        elif self.state is 'move_to_kitchen':
            if self.move_abs.state is 'finish':
                self.change_state('repeat_order')

        elif self.state is 'repeat_order':
            temp = ''
            if self.order['table one'] != []:
                temp += 'Table one order'
                temp += " and ".join(self.order['table one'])
                temp += ". "
            if self.location_list['table two'] != []:
                temp += 'Table two order'
                temp += " and ".join(self.order['table two'])
                temp += ". "
            if self.location_list['table three'] != []:
                temp += 'Table three order'
                temp += " and ".join(self.order['table three'])
                temp += ". "
            if temp != '':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say(temp)
                self.change_state("wait_repeat_order")


                # elif self.state is 'wait_for_barman_first':
                #     if perception_data.device is self.Devices.VOICE

                # elif self.state is 'wait_for_order':
                #     self.say.say('I will go to ' + self.command + '.')

                # elif self.state is 'move_to_gpsr_start':
                #     if self.moveTo.state is 'finish':
                #         self.change_state('wait_for_command')
                # elif perception_data.device is self.Devices.VOICE:
                #     if 'robot stop' == perception_data.input:
                #         self.follow.stop()

                # def add_waving_people(self, tables ,points):
                #     for point in points:
                #         point_tf = self.tf_listener.transformPoint('map', point)
                #         # for i in self.waving_people:
                #         #     if not self.is_overlap(i, point):
                #         #         self.waving_people.append()
