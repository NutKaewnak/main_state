import rospy

from include.abstract_task import AbstractTask
from include.delay import Delay
from include.get_distance import get_distance
from math import hypot

__author__ = 'cin'


class RestaurantVDO(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.location_list = {'table a': [], 'table b': [], 'table c': [], 'kitchen bar': []}
        self.items = ['apple', 'banana', 'orange', 'cookie', 'coke', 'mike', 'soda', 'ice cream']
        self.table_order = {'table a': [], 'table b': [], 'table c': []}
        self.serve_table = []
        self.list_table = []
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'Say')
            self.subtask.say('i\'m ready for commands.')
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if self.subtask.state is 'finish':
                if perception_data.device is self.Devices.VOICE:
                    print perception_data.input
                    if 'follow me' in perception_data.input:
                        self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                        self.follow = self.subtaskBook.get_subtask(self, 'FollowLeg')
                        self.change_state('follow_init')
                    elif 'stand by' in perception_data.input:
                        self.subtaskBook.get_subtask(self, 'Say').say('I will be waiting.')
                        self.change_state('stand_by_mode')

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE_LEG:
                # print 'hi'
                min_distance = 99
                self.track_id = -1
                for person in perception_data.input.people:
                    print 'person = ', person
                    if (person.pos.x > 0.8 and person.pos.x < 1.8
                        and person.pos.y > -0.5 and person.pos.y < 0.5):
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
                if perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(0, 0)
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('Where is this place ?')
                    self.change_state('ask_for_location')

                if perception_data.device is self.Devices.PEOPLE_LEG and perception_data.input.people:
                    print 'track_id =', self.track_id
                    for person in perception_data.input.people:
                        print ' person.id =', person.object_id
                        if self.track_id == person.object_id:
                            break
                        elif self.follow.guess_id == person.object_id:
                            self.track_id = self.follow.guess_id
                            print 'change track id = ', self.track_id
                if perception_data.device is self.Devices.NAVIGATE and perception_data.input:
                    print perception_data.input

        elif self.state is 'ask_for_location':
            if self.subtask.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location
                        self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                        self.subtask.say('This is ' + location + ' yes or no ?')
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if self.subtask.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                self.change_state('wait_for_command')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                self.subtask.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

        elif self.state is 'stand_by_mode':
            if perception_data.device is self.Devices.VOICE:
                if 'take order' in perception_data.input:
                    for location in self.location_list:
                        if location in perception_data.input:
                            self.list_table.append(location)
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m going to ' + self.list_table[0])
                    self.change_state('go_take_order')

                elif 'serve order' in perception_data.input:
                    for location in self.location_list:
                        if location in perception_data.input:
                            self.serve_table.append(location)
                    self.subtaskBook.get_subtask(self, 'Say').say('I\'m going to ' + self.serve_table[0])
                    self.change_state('go_serving_order')

        elif self.state is 'go_take_order':
            if self.list_table:
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveBaseAbsolute')
                self.subtask.set_position(self.location_list[self.list_table[0]])
                self.change_state('reach_table')
            elif not self.list_table:
                self.subtaskBook.get_subtask(self, 'Say').say('I\'m moving back to kitchen bar.')
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveBaseAbsolute')
                self.subtask.set_position(self.location_list['kitchen bar'])

        elif self.state is 'reach_table':
            if perception_data.device is 'BASE_STATUS':
                if perception_data.input.status_list[0].status is 3:
                    self.subtaskBook.get_subtask(self, 'Say').say('I reach ' + self.list_table[0] + ' and ready to take order.')
                    self.command = self.list_table.pop(0)
                    print self.command
                    self.state = 'take_order'

        elif self.state is 'take_order':
            if perception_data.device is 'VOICE':
                for item in self.items:
                    if item in perception_data.input:
                        self.table_order[self.command].append(item)
                # print 'table_order' + self.table_order[self.command]
                foods = ""
                for food in self.table_order[self.command]:
                    foods += food + " "
                print 'foods =' + foods
                self.subtaskBook.get_subtask(self, 'Say').say('Is your order ' + foods + ' yes or no?')
                self.change_state('confirm_order')

        elif self.state is 'confirm_order':
            if perception_data.device is 'VOICE':
                if 'robot yes' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I remember that.')
                    self.state = 'go_take_order'
                elif 'robot no' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('sorry, What are your order?')
                    self.change_state('take_order')

        elif self.state is 'go_serving_order':
            if self.serve_table:
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveBaseAbsolute')
                self.subtask.set_position(self.location_list[self.serve_table[0]])
                self.change_state('serve_order')
            elif not self.serve_table:
                self.subtaskBook.get_subtask(self, 'Say').say('I\'m moving to kitchen bar.')
                self.change_state('stand_by_mode')

        elif self.state is 'serve_order':
            if self.subtask.state is 'succeeded':
                foods = ""
                for item in self.table_order[self.serve_table[0]]:
                    foods += item + ' '
                self.subtaskBook.get_subtask(self, 'Say').say('Order is ' + foods + 'please take it and if you finish please say. I\'ve already take my order.')
                self.change_state('confirm_receive_food')

        elif self.state is 'confirm_receive_food':
            if perception_data.device is self.Devices.VOICE and 'I\'ve already take my order' in perception_data.input:
                self.subtaskBook.get_subtask(self, 'Say').say('Ok, I\'m moving.')
                self.change_state('go_serving_order')


