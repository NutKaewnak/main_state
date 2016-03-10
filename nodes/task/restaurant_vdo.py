import rospy
from include.abstract_task import AbstractTask
from include.get_distance import get_distance
from include.delay import Delay
from std_msgs.msg import Float64

__author__ = 'Nicole'


class RestaurantVDO(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.location = None
        self.init_location = None
        self.location_list = {'location one': [], 'location two': [], 'location three': []}
        self.command = None
        self.count = 0
        self.first = None
        self.say = None
        self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.change_state('wait_for_command')

        elif self.state is 'follow_init':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.PEOPLE:
                distance = 3.0  # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.follow.set_person_id(id)
                    self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if self.say.state is not 'finish':
                return
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 2  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = get_distance(person.personpoints, self.follow.last_point)
                    if distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE:
                if 'robot stop' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Where is this place ?')
                    self.change_state('ask_for_location')
                elif 'robot waiting' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Wait for command.')
                    self.change_state('wait_for_command')

        elif self.state is 'ask_for_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                for location in self.location_list:
                    if location in perception_data.input:
                        self.location = location
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('This is ' + location + ' yes or no ?')
                        self.change_state('confirm_location')

        elif self.state is 'confirm_location':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I remember ' + self.location + '.')
                self.location_list[self.location] = self.perception_module.base_status.position
                print self.location_list
                self.change_state('init')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , Where is this place ?')
                self.change_state('ask_for_location')

        elif self.state is 'wait_for_command':
            if self.say.state is not 'init' and self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE:
                print perception_data.input
                print self.location_list
                for location in self.location_list:
                    if location in perception_data.input:
                        self.command = location
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('bring cup noodle to ' + self.command + ' yes or no ?')
                        self.change_state('confirm_command')

                if 'follow me' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('I will follow you.')
                    self.change_state('follow_init')
                elif 'get out' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('I will go back.')
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.move = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                    self.move.to_location('gpsr_start')
                    self.change_state('move_to_gpsr_start')

        elif self.state is 'confirm_command':
            if self.say.state is not 'finish':
                return
            if perception_data.device is self.Devices.VOICE and 'robot yes' in perception_data.input:
                self.mama()
                self.pub_left_gripper.publish(1.1)
                rospy.sleep(5)
                self.pub_left_gripper.publish(-0.4)
                rospy.sleep(3)
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I will go to ' + self.command + '.')
                self.move = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.move.set_position(self.location_list[self.command][0], self.location_list[self.command][1], self.location_list[self.command][2])
                self.change_state('move_to_first')
            elif perception_data.device is self.Devices.VOICE and 'robot no' in perception_data.input:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Sorry , What did you say ?')
                self.change_state('wait_for_command')

        elif self.state is 'move_to_first':
            if self.move.state is 'finish':
                self.change_state('wait_for_order')

        elif self.state is 'move_to_gpsr_start':
            if self.current_subtask.state is 'finish':
                self.change_state('wait_for_command')
