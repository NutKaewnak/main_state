import rospy

from include.abstract_task import AbstractTask
from include.delay import Delay
from include.get_distance import get_distance
from math import hypot, sqrt, atan2
from geometry_msgs.msg import Pose2D, Vector3

__author__ = 'cin'


class RestaurantCin(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.last_point = Vector3()
        self.location_list = {'table a': [], 'table b': [], 'table c': [], 'kitchen bar': []}
        self.items = ['green tea', 'cookie', 'coke', 'snack', 'water']
        self.table_order = {'table a': [], 'table b': [], 'table c': []}
        self.ordered_table = []
        self.serve_table = []
        self.list_table = []
        self.delay = Delay()
        self.side = None

    def perform(self, perception_data):
        # print self.state
        if self.is_performing:
            return
        self.is_performing = True

        if self.state is 'init':
            rospy.loginfo('--------------------init--------------')
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('i\'m ready for commands.')
            self.change_state('wait_for_command')
            # self.command = 'table a'
            # self.change_state('take_order')

        elif self.state is 'wait_for_command':
            # if self.subtask.state is 'finish':
            # print perception_data.device
            # print self.state
            if perception_data.device is self.Devices.VOICE:
                if 'lamyai follow me' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                    self.change_state('send_info')
                elif 'lamyai standby mode' in perception_data.input:
                    self.change_state('init_stand_by_mode')

# ----------------------------------------------------------------------------------------------------------------------
# follow phase
        elif self.state is 'send_info':
            # print self.state
            self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', '', [])
            self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
            self.change_state('follow_init')

        elif self.state is 'follow_init':
            # print self.current_subtask
            if perception_data.device is self.Devices.PEOPLE_LEG:
                min_distance = 99
                self.track_id = -1
                for person in perception_data.input.people:
                    # print person.pos.x, person.pos.y
                    if 0.8 < person.pos.x < 1.8 and -0.7 < person.pos.y < 0.7:
                        distance = hypot(person.pos.x, person.pos.y)
                        print 'person id =', person.object_id
                        if distance < min_distance:
                            self.track_id = person.object_id
                if self.track_id != -1:
                    print 'track_id' + self.track_id
                    self.follow.set_person_id(self.track_id)
                    self.change_state('follow')

        elif self.state is 'follow':
            # print 'follow state =' + self.follow.state
            # recovery follow
            # print self.state
            if perception_data.device is self.Devices.VOICE and 'lamyai stop' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                self.subtaskBook.get_subtask(self, 'Say').say('Where is this place ?')
                self.change_state('ask_for_location')

            if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input.people:
                for person in perception_data.input.people:
                    # print ' person >>>>>>>>> =', self.track_id
                    # print ' follow guess_id =', self.follow.guess_id
                    # print 'person.object_id =', person.object_id
                    if self.track_id == person.object_id:
                        break
                    elif self.follow.guess_id == person.object_id:
                        self.track_id = self.follow.guess_id
                        print 'change track id = ', self.track_id
            if perception_data.device is self.Devices.NAVIGATE and perception_data.input:
                print perception_data.input

        elif self.state is 'ask_for_location':
            # print self.state
            if self.subtask.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        # print perception_data.input
                        self.location = location
                        self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                        self.subtask.say('Where is ' + self.location + '?')
                        self.change_state('get_location_side')

        elif self.state is 'get_location_side':
            if perception_data.device is self.Devices.VOICE:
                if 'right' in perception_data.input or 'left' in perception_data.input:
                    self.side = perception_data.input.replace("my", "your")
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say(self.location + ' is ' + self.side + '. yes or no ?')
                    self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            # print self.state
            if self.subtask.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'lamyai yes' in perception_data.input:
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                print self.location_list[self.location]
                # print self.perception_module.base_status.position
                if 'left' in self.side:
                    self.location_list[self.location] = (
                    self.perception_module.base_status.position[0], self.perception_module.base_status.position[1],
                    self.perception_module.base_status.position[2] - 1.6)

                    # self.direction_list[self.location] = 'left'
                else:
                    self.location_list[self.location] = (
                    self.perception_module.base_status.position[0], self.perception_module.base_status.position[1],
                    self.perception_module.base_status.position[2] + 1.6)
                self.change_state('wait_for_command')
            elif perception_data.device is self.Devices.VOICE and 'lamyai no' in perception_data.input:
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

# ----------------------------------------------------------------------------------------------------------------------
# standby phase
        elif self.state is 'init_stand_by_mode' and self.location_list['kitchen bar']:
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            self.subtask.set_position(self.location_list['kitchen bar'][0], self.location_list['kitchen bar'][1],
                                      self.location_list['kitchen bar'][2])
            self.change_state('ready_to_standby')

        elif self.state is 'ready_to_standby':
            if self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('I will be waiting.')
                self.subtaskBook.get_subtask(self, 'WebCommu').send_info('standby', '', [])
                self.change_state('stand_by_mode')
            elif self.subtask.state is 'error':
                self.change_state('init_stand_by_mode')

        elif self.state is 'stand_by_mode':
            if perception_data.device is self.Devices.VOICE:
                if 'lamyai take order' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('Where should i go?')
                    self.change_state('table_order')
                elif 'lamyai go to serve order' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('Where should i go?')
                    self.change_state('table_serve')

# ----------------------------------------------------------------------------------------------------------------------
# take order phase
        elif self.state is 'table_order':
            if perception_data.device is self.Devices.VOICE:
                if not self.list_table or 'please' not in perception_data.input:
                    for location in self.location_list:
                        if location in perception_data.input and location not in self.list_table and location != 'kitchen bar':
                            self.table = location
                            self.list_table.append(location)
                            print 'table' + str(self.table)
                    print self.list_table
                    self.change_state('chk_table')
                elif self.list_table and 'please' in perception_data.input:
                    print self.list_table
                    table = ''
                    for lis in self.list_table:
                        table += lis + ' '
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m going to ' + table)
                    self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', '', [])
                    self.change_state('go_take_order')

        # elif self.state is 'chk_table':
        #     if not perception_data.device is 'VOICE':
        #         self.subtaskBook.get_subtask(self, 'Say').say(self.table)
        #         self.change_state('table_order')

        elif self.state is 'chk_table':
            if perception_data.device is self.Devices.VOICE:
                if self.list_table and 'please' in perception_data.input:
                    print self.list_table
                    table = ''
                    for lis in self.list_table:
                        table += lis + ' '
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m going to ' + table)
                    self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', '', [])
                    self.state = 'go_take_order'
                else:
                    for location in self.location_list:
                        if location in perception_data.input and location not in self.list_table:
                            print location
                            self.list_table.append(location)
                    print self.list_table
                    self.state = 'table_order'

        elif self.state is 'go_take_order':
            if self.list_table:
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.subtask.set_position(self.location_list[self.list_table[0]][0],
                                          self.location_list[self.list_table[0]][1],
                                          self.location_list[self.list_table[0]][2])
                self.change_state('reach_table')
            elif not self.list_table and self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('I\'m moving back to kitchen bar.')
                # self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                # self.subtask.set_position(self.location_list['kitchen bar'][0], self.location_list['kitchen bar'][1],
                #                           self.location_list['kitchen bar'][2])
                self.change_state('init_stand_by_mode')

        elif self.state is 'reach_table':
            if perception_data.device is self.Devices.BASE_STATUS:
                if perception_data.input is 3:
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('I reach ' + self.list_table[0] +
                                                                  ' and ready to take order.')
                    self.command = self.list_table.pop(0)
                    self.ordered_table.append(self.command)
                    print self.command
                    self.change_state('take_order')

        elif self.state is 'take_order':
            if perception_data.device is 'VOICE' and self.subtask.state is 'finish':
                if not self.table_order[self.command] or 'please' not in perception_data.input:
                    for item in self.items:
                        if item in perception_data.input and item not in self.table_order[self.command]:
                            # self.item_order = item
                            self.table_order[self.command].append(item)
                            self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', self.command,
                                                                                     self.table_order[self.command])
                    print self.table_order[self.command]
                    self.change_state("chk_order")
                elif self.table_order[self.command] and 'please' in perception_data.input:
                    print self.table_order[self.command]
                    foods = ""
                    for food in self.table_order[self.command]:
                        foods += food + " "
                    print 'foods =' + foods
                    self.subtaskBook.get_subtask(self, 'Say').say('Is your order ' + foods + ' yes or no?')
                    self.change_state('confirm_order')
        #
        # elif self.state is 'chk_sound_take_order':
        #     if not perception_data.device is 'VOICE':
        #         self.subtaskBook.get_subtask(self, 'Say').say(self.item_order)
        #         self.change_state('take_order')

        elif self.state is 'chk_order':
            if perception_data.device is 'VOICE':
                if self.table_order[self.command] and 'please' in perception_data.input:
                    foods = ""
                    for food in self.table_order[self.command]:
                        foods += food + " "
                    print 'foods =' + foods
                    self.subtaskBook.get_subtask(self, 'Say').say('Is your order ' + foods + ' yes or no?')
                    self.state = 'confirm_order'
                else:
                    for item in self.items:
                        if item in perception_data.input and item not in self.table_order[self.command]:
                            self.table_order[self.command].append(item)
                            self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', self.command,
                                                                                     self.table_order[self.command])
                    print self.table_order[self.command]
                    self.state = 'take_order'

        elif self.state is 'confirm_order':
            if perception_data.device is 'VOICE':
                if 'lamyai yes' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('I remember that.')
                    self.state = 'go_take_order'
                elif 'lamyai no' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('sorry, What are your order?')
                    self.table_order[self.command] = []
                    self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', self.command,
                                                                             self.table_order[self.command])
                    self.change_state('take_order')

# ----------------------------------------------------------------------------------------------------------------------
# give order phase
        elif self.state is 'give_order1':
            if perception_data.device is self.Devices.BASE_STATUS:
                if perception_data.input is 3:
                    self.state = 'give_order2'

        elif self.state is 'give_order2':
            if self.ordered_table:
                self.state = "tell_barman"
            elif not self.ordered_table:
                self.state = "stand_by_mode"

        elif self.state is 'tell_barman':
            table = self.ordered_table.pop(0)
            foods = ''
            for food in self.table_order[table]:
                foods += food + ' '
            self.subtaskBook.get_subtask(self, 'Say').say(table + ' orders' + foods)
            self.state = "give_order2"

# ----------------------------------------------------------------------------------------------------------------------
# serve order
        elif self.state is 'table_serve':
            if perception_data.device is 'VOICE':
                if not self.serve_table or 'please' not in perception_data.input:
                    for location in self.location_list:
                        if location in perception_data.input:
                            self.serve_list = location
                            self.serve_table.append(location)
                    print self.serve_table
                    self.state = "chk_table_serve"
                elif self.serve_table and 'please' in perception_data.input:
                    print self.serve_table
                    table = ""
                    for lis in self.serve_table:
                        table += lis + " "
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m going to ' + table)
                    self.state = 'go_serving_order'

        elif self.state is 'chk_table_serve':
            if perception_data.device is 'VOICE':
                if self.serve_table and 'please' in perception_data.input:
                    print self.serve_table
                    table = ''
                    for lis in self.serve_table:
                        table += lis + " "
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m going to ' + table)
                    self.state = 'go_serving_order'
                else:
                    for location in self.location_list:
                        if location in perception_data.input:
                            print location
                            self.serve_table.append(location)
                    print self.serve_table
                    self.state = 'table_serve'
            if perception_data.device is 'VOICE':
                pass
        #
        # elif self.state is 'chk_sound_serve':
        #     if not perception_data.device is 'VOICE':
        #         self.subtaskBook.get_subtask(self, 'Say').say(self.serve_list)
        #         self.change_state('table_serve')

        elif self.state is 'go_serving_order':
            self.subtaskBook.get_subtask(self, 'WebCommu').send_info('active', self.command,
                                                                   self.table_order[self.command])
            if self.serve_table:
                self.change_state('go_serving_order1')
                self.command = self.serve_table.pop(0)
            elif not self.serve_table:
                self.subtaskBook.get_subtask(self, 'Say').say('I\'m moving to kitchen bar.')
                # self.subtaskBook.get_subtask(self, 'WebCommu').send_info('finish', '', [])
                self.change_state('init_stand_by_mode')

        elif self.state is 'go_serving_order1':
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
            self.subtask.set_position(self.location_list[self.command][0], self.location_list[self.command][1],
                                      self.location_list[self.command][2])
            self.change_state('serve_order')

        elif self.state is 'serve_order':
            if self.subtask.state is 'finish':
                foods = ''
                print self.table_order
                print self.command
                for item in self.table_order[self.command]:
                    foods += item + ' '
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('Order is ' + foods + 'please take it and if you finish.'
                                                       ' please say. I\'ve already take my order.')
                self.change_state('confirm_receive_food')
            elif self.subtask.state is 'error':
                self.change_state('go_serving_order1')

        elif self.state is 'confirm_receive_food':
            if perception_data.device is self.Devices.VOICE and 'i\'ve already take my order' in perception_data.input \
                    and self.subtask.state is 'finish':
                self.subtaskBook.get_subtask(self, 'Say').say('Ok, I\'m moving.')
                self.subtaskBook.get_subtask(self, 'WebCommu').send_info('finish', self.command, [])
                self.change_state('go_serving_order')


