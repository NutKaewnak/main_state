from include.abstract_task import AbstractTask
from include.delay import Delay

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
        self.food = ['noodles', 'peanuts', 'hamburger', 'fries', 'orange juice', 'water']
        self.say = self.subtaskBook.get_subtask(self, 'Say')
        self.follow = self.subtaskBook.get_subtask(self, 'FollowMe')
        self.moveTo = self.subtaskBook.get_subreltask(self, 'MoveToLocation')
        self.moveAbs = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
        self.move_relative = self.subtaskBook.get_subtask(self, 'MoveRelative')
        self.search_waving_people = self.subtaskBook.get_subtask(self, 'SearchWavingPeople')
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('wait_for_command')

        elif self.state is 'follow_init':
            if self.say.state is not 'finish':
                return
            self.follow.start()
            self.change_state("follow")

        elif self.state is 'follow':
            if perception_data.device is self.Devices.VOICE:
                if 'robot stop' in perception_data.input:
                    # self.say = self.subtaskBook.get_subtask(self, 'Say')
                    if self.location_list['location one'] != [] and self.location_list['location two'] != [] and self.location_list['location three'] != []:
                        self.say.say('I am at the kitchen. Is it on your left or on your right ?')
                        self.change_state('ask_for_kitchen')
                    else:
                        self.say.say('Where is this place ?')
                        self.change_state('ask_for_location')
                elif 'robot waiting' in perception_data.input:
                    # self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Wait for command.')
                    self.change_state('wait_for_command')

        elif self.state is 'ask_for_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location.replace("my", "your")
                        # self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say(self.location + '. yes or no ?')
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                if 'left' in self.location:
                    self.location_list[self.location][2] += 1.57
                    # self.direction_list[self.location] = 'left'
                else:
                    self.location_list[self.location][2] -= 1.57
                    # self.direction_list[self.location] = 'right'
                print self.location_list
                # print self.direction_list
                self.change_state('init')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

        elif self.state is 'ask_for_kitchen':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                if 'left' in perception_data.input:
                    self.location = 'kitchen is on your left'
                     # self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say(self.location + '. yes or no ?')
                    self.change_state('confirm_kitchen')
                elif 'right' in perception_data.input:
                    self.location = 'kitchen is on your right'
                     # self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say(self.location + '. yes or no ?')
                    self.change_state('confirm_kitchen')

        elif self.state is 'confirm_kitchen':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                if 'left' in self.location:
                    self.location_list[self.location][2] += 1.57
                    # self.direction_list[self.location] = 'left'
                else:
                    self.location_list[self.location][2] -= 1.57
                    # self.direction_list[self.location] = 'right'
                print self.location_list
                # print self.direction_list
                self.change_state('wait_for_barman_first')

            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , Is it on your left or on your right ?')
                self.change_state('ask_for_kitchen')

        elif self.state is 'wait_for_command':
            # if self.say.state is not 'init' and self.say.state is not 'finish':
            #     return
            if perception_data.device is self.Devices.VOICE:
                if 'follow me' in perception_data.input:
                    # self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('I will follow you.')
                    self.change_state('follow_init')

        elif self.state is 'wait_for_barman_first':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                print perception_data.input
                print self.location_list
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = location
                        # self.say = self.subtaskBook.get_subtask(self, 'Say')
                        # self.say.say('bring cup noodle to ' + self.command + ' yes or no ?')
                        self.change_state('confirm_command')

        elif self.state is 'confirm_command':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I will go to ' + self.command + '.')
                self.current_table = self.command
                self.moveAbs.set_position(self.location_list[self.command][0], self.location_list[self.command][1], self.location_list[self.command][2])
                self.change_state('move_to_location')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , What did you say ?')
                self.change_state('wait_for_barman_first')

        elif self.state is 'move_to_location':
            if self.moveAbs.state is 'finish':
                # self.delay.wait(3)
                # self.change_state('wait_for_order')
                self.change_state('turning_1')

        elif self.state is 'turning_1':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_1')

        elif self.state is 'waving_1' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_1')

        elif self.state is 'wait_for_waving_1':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_2')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_2')

        elif self.state is 'turning_2':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_2')

        elif self.state is 'waving_2' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_2')

        elif self.state is 'wait_for_waving_2':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_3')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_3')

        elif self.state is 'turning_3':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_3')

        elif self.state is 'waving_3' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_3')

        elif self.state is 'wait_for_waving_3':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_4')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_4')

        elif self.state is 'turning_4':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_4')

        elif self.state is 'waving_4' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_4')

        elif self.state is 'wait_for_waving_4':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_5')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_5')

        elif self.state is 'turning_5':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_5')

        elif self.state is 'waving_5' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_5')

        elif self.state is 'wait_for_waving_5':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_6')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_6')

        elif self.state is 'turning_6':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_6')

        elif self.state is 'waving_6' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_6')

        elif self.state is 'wait_for_waving_6':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_7')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_7')

        elif self.state is 'turning_7':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_7')

        elif self.state is 'waving_7' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_7')

        elif self.state is 'wait_for_waving_7':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_8')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_8')

        elif self.state is 'turning_8':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_8')

        elif self.state is 'waving_8' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_8')

        elif self.state is 'wait_for_waving_8':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_9')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_9')

        elif self.state is 'turning_9':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_9')

        elif self.state is 'waving_9' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_9')

        elif self.state is 'wait_for_waving_9':
            if self.search_waving_people.state is 'not_found':
                self.change_state('turning_10')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('turning_10')

        elif self.state is 'turning_10':
            self.move_relative.set_position(0, 0, 0.628)
            self.delay.wait(3)
            self.change_state('waving_10')

        elif self.state is 'waving_10' and not self.delay.is_waiting():
            self.search_waving_people.start()
            self.change_state('wait_for_waving_10')

        elif self.state is 'wait_for_waving_10':
            if self.search_waving_people.state is 'not_found':
                self.change_state('say_for_order')
            elif self.search_waving_people.state is 'finish':
                if not self.search_waving_people.get_point() == None:
                    self.waving_people.append(self.search_waving_people.get_point()) #!!!!!!
                self.change_state('say_for_order')

        elif self.state is 'say_for_order':
            self.say.say('Hello sir, What order you will take ?')
            self.change_state('wait_for_order')

        elif self.state is 'wait_for_order':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for food in self.food:
                    if self.food in perception_data.input:
                        self.order[self.current_table].append(food)
                if self.order[self.current_table] == []:
                    return
                else:
                    self.change_state('ask_for_order')
                # self.say.say('Your orders are ' + " and ".join(self.order[self.current_table]))

        elif self.state is 'ask_for_order':
            self.say.say('Do you want ' + " and ".join(self.order[self.current_table]) + ' ?')
            self.change_state('confirm_for_order')

        elif self.state is 'confirm_for_order':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Ok')
                if self.stack_table is not None:
                    # self.say.say('I will go to ' + self.stack_table + ' to get a order.')
                    self.change_state('set_to_waving_table')
                else:
                    self.change_state('move_to_kitchen')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                # self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , What did you say ?')
                self.change_state('wait_for_order')

        elif self.state is 'set_to_waving_table':
            if self.say.state is not 'finish':
                return
            if self.stack_table is not None:
                self.say.say('I will go to ' + self.stack_table + ' to get a order.')
                self.moveAbs.set_position(self.location_list[self.stack_table][0], self.location_list[self.stack_table][1], self.location_list[self.stack_table][2])
                self.current_table = self.stack_table
                self.change_state('move_to_waving_table')

        elif self.state is 'move_to_waving_table':
            if self.moveAbs.state is 'finish':
                self.change_state('say_for_order')

        elif self.state is 'set_to_kitchen':
            if self.say.state is not 'finish':
                return
            if self.stack_table is not None:
                self.say.say('I will go back to Kitchen .')
                self.moveAbs.set_position(self.location_list['kitchen'][0], self.location_list['kitchen'][1], self.location_list['kitchen'][2])
                self.current_table = self.stack_table
                self.change_state('move_to_kitchen')

        elif self.state is 'move_to_kitchen':
            if self.moveAbs.state is 'finish':
                self.change_state('repeat_order')

        elif self.state is 'repeat_order':
            temp = ''
            if self.location_list['table one'] != []:
                temp += " and ".join(self.location_list['table one'])
                temp += ". "
            if self.location_list['table two'] != []:
                temp += " and ".join(self.location_list['table two'])
                temp += ". "
            if self.location_list['table three'] != []:
                temp += " and ".join(self.location_list['table three'])
                temp += ". "
            if temp != '':
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
